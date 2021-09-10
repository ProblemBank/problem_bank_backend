from Game.serializers import CheckableObjectSerializer, FamousPersonSerializer
from Game.models import CheckableObject, GameProblem, Player
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from problembank.permissions import DefualtPermission
from problembank.models import *
from rest_framework import permissions
# from problembank.views import permissions as customPermissions
from problembank.serializers import *
from django.utils import timezone
import sys
from itertools import chain
# data['juged_by'] = request.user.account #just for mentor not all the times!


def get_random_problem_from_group(gid, account):
    try:
        problem_group = ProblemGroup.objects.filter(id=gid)[0]
    except:
        return Response({"message":"چنین مسئله ای وجود ندارد."},status=status.HTTP_400_BAD_REQUEST)

    problems = problem_group.problems.all().select_subclasses()
    submit = None
    try: 
        submit = AutoCheckSubmit.objects.all().select_subclasses().filter(problem_group=gid, respondents__in=[account])[0]
        submit = AutoCheckSubmitSerializer(submit).data
    except:
        pass
    try: 
        submit = JudgeableSubmit.objects.all().select_subclasses().filter(problem_group=gid, respondents__in=[account])[0]
        submit = JudgeableSubmitSerializer(submit).data
    except:
        pass
    if submit is not None:
        if submit['status'] != 'Received':
                return Response({"message":"شما قبلا از اینجا مسئله دریافت کرده اید و پاسخ آن را فرستاده اید."},status=status.HTTP_400_BAD_REQUEST)
        else:
            problem = Problem.objects.all().select_subclasses().filter(id=submit['problem'])[0]
            problem_data = ProblemSerializer(problem).data
            data = {}
            problem_data.pop('answer')
            data['problem'] = problem_data
            data['submit'] = submit
            return Response(data, status=status.HTTP_200_OK)
    
    player = Player.objects.filter(users__in=[account.user])[0]
    if player.coin < 1000 and not gid in mashahir_ids:
        return Response({"message":"سکه شما کافی نیست."},status=status.HTTP_400_BAD_REQUEST)
    try:
        return problems.order_by('?')[0]
    except:
        return Response({"message":"گروه مسئله خالی است."},status=status.HTTP_400_BAD_REQUEST)



mashahir_ids = []
def get_problem_cost(problem):
    return 0 if problem.groups.filter(id__in=mashahir_ids) else 1000

def get_problem_reward(problem):
    return 400 if problem.groups.filter(id__in=mashahir_ids) else (
           1000 + (750 if problem.difficulty == Problem.Difficulty.Hard else 
                  (250 if problem.difficulty == Problem.Difficulty.Medium else 0)
                  )
            )
def add_reward_to_player(player, submit, problem):
    game_problem = GameProblem.objects.filter(problem_group=submit.problem_group)[0]
    merchandise = game_problem.reward_merchandise
    player.blue_toot += merchandise.blue_toot
    player.red_toot += merchandise.red_toot
    player.black_toot += merchandise.black_toot
    player.coin += get_problem_reward(problem)
    if game_problem.famous_person is not None:
        player.famous_persons.add(game_problem.famous_person)
    player.save()

def remove_merchandise_from_player(player, object):
    merchandise = object.merchandise
    if len(player.checkable_objects.all().filter(id=object.id)) > 0:
            return False, Response({"message":"قبلا این شی را بررسی کرده اید!"},status=status.HTTP_400_BAD_REQUEST)
        
    if  player.coin < merchandise.coin or\
            player.blue_toot < merchandise.blue_toot or\
            player.red_toot < merchandise.red_toot or\
            player.black_toot < merchandise.black_toot:

        return False, Response({"message":"توت شما کافی نیست!"},status=status.HTTP_400_BAD_REQUEST)    

    player.coin -= merchandise.coin
    player.blue_toot -= merchandise.blue_toot
    player.red_toot -= merchandise.red_toot
    player.black_toot -= merchandise.black_toot
    player.save()
    return True, Response(status=status.HTTP_200_OK)
    
@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def is_problem_goten_from_group(request, gid):
    account = request.user.account
    submit = None
    try: 
        submit = AutoCheckSubmit.objects.all().select_subclasses().filter(problem_group=gid, respondents__in=[account])[0]
        submit = AutoCheckSubmitSerializer(submit).data
    except:
        pass
    try: 
        submit = JudgeableSubmit.objects.all().select_subclasses().filter(problem_group=gid, respondents__in=[account])[0]
        submit = JudgeableSubmitSerializer(submit).data
    except:
        pass
    if submit is not None:
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_problem_from_group(request, gid):
    account = request.user.account
    problem = get_random_problem_from_group(gid, account)
    if not issubclass(problem.__class__, Problem):
        return problem
    serializerClass = BaseSubmitSerializer.get_serializer(problem.problem_type)
    data = {}
    data['problem'] = problem.pk
    data['problem_group'] = gid
    data['respondents'] = []
    serializer = serializerClass(data=data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    instance = serializer.create(serializer.validated_data)
    player = Player.objects.filter(users__in=[account.user])[0]
    for user in player.users.all():
        instance.respondents.add(user.account)
    instance.save()
    player.coin = player.coin - get_problem_cost(problem)
    player.save()
    data = {}
    data['problem'] =  ProblemSerializer(problem).data
    data['submit'] = serializerClass(instance).data
    data['problem'].pop('answer')
    return Response(data, status=status.HTTP_200_OK)
    
@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_answer(request, sid, pid):
    data = {}
    data['id'] = sid
    data['problem'] = pid
    try:
        problem = Problem.objects.filter(id=pid)[0]
    except:
        return Response({"message":"مسئله موجود نیست!"},status=status.HTTP_400_BAD_REQUEST)
    serializerClass = BaseSubmitSerializer.get_serializer(problem.problem_type)
    try:
        instance = serializerClass.Meta.model.objects.filter(id=sid)[0]
    except:
        return Response({"message":"ابتدا باید صورت مسئله را دریافت کنید."},status=status.HTTP_400_BAD_REQUEST)
    if len(instance.respondents.all().filter(id=request.user.account.id)) == 0:
        return Response({"message":"این پاسخ مربوط به شما نیست!"},status=status.HTTP_400_BAD_REQUEST)
    if serializerClass == AutoCheckSubmitSerializer:
        data['answer'] = {}
        try:
            data['answer']['text'] = request.data['text']
        except:
            data['answer']['text'] = "بدون پاسخ تایپی"
    else:
        data['text_answer'] = {}
        try:
            data['text_answer']['text'] = request.data['text']
        except:
            data['text_answer']['text'] = "بدون پاسخ تایپی"
        data['upload_file_answer'] = {}
        try:
            data['upload_file_answer']['answer_file'] = request.FILES['file']
            data['upload_file_answer']['file_name'] = f'problem {pid} player {request.user.account.id}'
        except:
            data.pop('upload_file_answer')
    serializer = serializerClass(data=data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if instance.status != BaseSubmit.Status.Received:
        return Response({"message":"قبلا پاسخ این مسئله را ارسال کرده اید!"},status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data
    instance = serializer.update(instance, data)
    if instance.mark == 1:
        player = Player.objects.filter(users__in=[request.user])[0]
        add_reward_to_player(player, instance, problem)
        
    instance.save()
    response = serializer.to_representation(instance)
    return Response(response ,status=status.HTTP_200_OK)

@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def judge(request, sid , mark):
    account = request.user.account
    submit = JudgeableSubmit.objects.filter(id=sid)[0]
    if submit.status == BaseSubmit.Status.Received:
        return Response({"message":"هنوز پاسخی برای این مسئله ارسال نشده است."},status=status.HTTP_400_BAD_REQUEST)
    
    if submit.status == BaseSubmit.Status.Judged:
        return Response({"message":"این مسئله قبلا تصحیح شده است."},status=status.HTTP_400_BAD_REQUEST)
    submit.judged_at = timezone.now()
    submit.status = BaseSubmit.Status.Judged
    submit.judged_by = account
    submit.mark = mark
    submit.save()
    if submit.mark == 1:
        player = Player.objects.filter(users__in=[request.user])[0]
        problem = Problem.objects.filter(id=submit.problem.id)[0]
        add_reward_to_player(player, submit, problem)
    return 


@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ckeck_object(request, cid):
    try:
        object = CheckableObject.objects.filter(id=cid)[0]
    except:
        return Response({"message":"چنین شی ای وجود ندارد."},status=status.HTTP_400_BAD_REQUEST)
    player = Player.objects.filter(users__in=[request.user])[0]
    is_ok, responce = remove_merchandise_from_player(player, object)
    if is_ok:
        player.checkable_objects.add(object)
    return responce

@transaction.atomic
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_objects(request):
    player = Player.objects.filter(users__in=[request.user])[0]
    data = CheckableObjectSerializer(player.checkable_objects.all(), many=True).data
    return Response(data ,status=status.HTTP_200_OK)

@transaction.atomic
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_all_objects(request):
    data = CheckableObjectSerializer(CheckableObject.objects.all(), many=True).data
    return Response(data ,status=status.HTTP_200_OK)



@transaction.atomic
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_famous_persons(request):
    player = Player.objects.filter(users__in=[request.user])[0]
    data = FamousPersonSerializer(player.famous_persons.all(), many=True).data
    return Response(data ,status=status.HTTP_200_OK)

from Account.serializers import add_accounts, add_players

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, DefualtPermission])
def initial_players(request):
    try:
        add_accounts()
    except:
        pass
    add_players()