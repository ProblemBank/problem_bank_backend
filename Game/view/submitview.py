from django.core.checks import messages
from Game.serializers import CheckableObjectSerializer, FamousPersonSerializer, PrivateCheckableObjectSerializer
from Game.models import CheckableObject, GameProblem, Notification, Player
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from problembank.permissions import DefaultPermission
from problembank.models import *
from rest_framework import permissions
# from problembank.views import permissions as customPermissions
from problembank.serializers import *
from django.utils import timezone
import sys
from itertools import chain
# data['juged_by'] = request.user.account #just for mentor not all the times!

from Game.models import Player
from Game.models import GameProblem, Notification
from problembank.views import submitview as banksubmitview

mashahir_ids = [10, 11, 12, 13, 14, 15, 16, 30, 31, 32, 33, 34]

def game_problem_request_permission_chcker(gid, user):
    player = Player.objects.filter(users__in=[user])[0]
    if player.coin < 1000 and not gid in mashahir_ids:
        return False
    return True

def get_problem_cost(problem):
    return 0 if problem.groups.filter(id__in=mashahir_ids) else 1000

def get_problem_reward(problem):
    return 400 if problem.groups.filter(id__in=mashahir_ids) else (
           1000 + (750 if problem.difficulty == Problem.Difficulty.Hard else 
                  (250 if problem.difficulty == Problem.Difficulty.Medium else 0)
                  )
            )
def add_reward_to_player(user, submit, problem):
    player = Player.objects.filter(users__in=[user])[0]
        
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
    

def get_users(user):
    player = Player.objects.filter(users__in=[user])[0]
    return player.users.all()

def game_problem_request_handler(user, submit):
    for user in get_users(user):
        submit.respondents.add(user.account)
    submit.save()
    
    player = Player.objects.filter(users__in=[user])[0]
    player.coin = player.coin - get_problem_cost(submit.problem)
    player.save()

def game_submit_handler(submit, user, problem):
    if submit.mark == 1:
        add_reward_to_player(user, submit, problem)
    
    if problem.problem_type == Problem.Type.ShortAnswerProblem:
        send_notification(user, submit.problem_group, submit.mark)
    submit.save()
    
    player = Player.objects.filter(users__in=[user])[0]
    game_problem = GameProblem.objects.filter(problem_group=submit.problem_group)[0]
    if game_problem.famous_person is not None:
        player.famous_persons.add(game_problem.famous_person)
    player.save()

def game_judge_handler(submit):
    if submit.mark == 1:
        user = submit.respondents.all()[0].user
        player = Player.objects.filter(users__in=[user])[0]
        problem = Problem.objects.filter(id=submit.problem.id)[0]
        add_reward_to_player(player, submit, problem)
    for account in submit.respondents.all():
        send_notification(account.user, submit.problem_group, submit.mark)
    


@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def is_problem_goten_from_group(request, gid):
   return banksubmitview.is_problem_goten_from_group_view(request.user.account, gid)

@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_problem_from_group(request, gid):
    return banksubmitview.request_problem_from_group_view(request.user.account, gid,
                game_problem_request_handler, game_problem_request_permission_chcker)

@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_answer(request, sid, pid):
    data = {}
    data['text'] = request.data['text']
    data['file'] = request.FILES['file']
    return banksubmitview.submit_answer_view(request.user.account, data, sid, pid, game_submit_handler)
    
@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def judge_view(request, sid , mark):
   return banksubmitview.judge_view(request.user.account, sid, mark, game_judge_handler)

def send_notification(user, problem_group, mark):
    data = {}
    data['title'] = "مسئله شما تصحیح شد."
    mark = 'کامل' if mark == 1 else 'صفر'
    data['body'] = f"شما نمره {mark} را از  {problem_group.title} کسب کردید."
    data['user'] = user
    data['time'] = timezone.now()
    Notification.objects.create(**data)


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
    data = PrivateCheckableObjectSerializer(CheckableObject.objects.all(), many=True).data
    return Response(data ,status=status.HTTP_200_OK)


@transaction.atomic
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_famous_persons(request):
    player = Player.objects.filter(users__in=[request.user])[0]
    data = FamousPersonSerializer(player.famous_persons.all(), many=True).data
    return Response(data ,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def decrease_coin(request):
    player = Player.objects.filter(users__in=[request.user.id])
    player.coin -= 7500
    player.save()
    return Response(status=status.HTTP_200_OK)


from Game.serializers import NotificationSerializer
def send_note(user, message):
    data = {}
    data['title'] = "مسئله شما تصحیح شد."
    data['body'] = message
    data['user'] = user
    data['time'] = timezone.now()
    Notification.objects.create(**data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, DefaultPermission])
def notification_to_all(request):
    for account in BankAccount.objects.all():
        try:
            send_note(account.user, message=request['message'])
        except:
            pass
    return Response(status=status.HTTP_200_OK)
