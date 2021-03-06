from os import nice
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes

from problembank.models import *
from rest_framework import permissions
# from problembank.views import permissions as customPermissions
from problembank.serializers import *
from problembank.permissions import SubmitAnswerPermission, JudgePermission
from django.utils import timezone
import sys
from itertools import chain
# data['juged_by'] = request.user.account #just for mentor not all the times!
from problembank.permissions import DefualtPermission
class JudgeableSubmitView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JudgeableSubmitSerializer
    queryset = JudgeableSubmit.objects.filter(status=BaseSubmit.Status.Delivered)


class AutoCheckSubmitView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated, DefualtPermission]
    queryset = AutoCheckSubmit.objects.all()
    serializer_class = AutoCheckSubmitSerializer


def get_submit_from_group(gid, account):
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
    return submit

def get_submit_from_problem(pid, account):
    submit = None
    try: 
        submit = AutoCheckSubmit.objects.all().select_subclasses().filter(problem=pid, respondents__in=[account])[0]
        submit = AutoCheckSubmitSerializer(submit).data
    except:
        pass
    try: 
        submit = JudgeableSubmit.objects.all().select_subclasses().filter(problem=pid, respondents__in=[account])[0]
        submit = JudgeableSubmitSerializer(submit).data
    except:
        pass
    return submit


def get_random_problem_from_group(gid, account):
    if not ProblemGroup.objects.filter(id=gid).exists():
        return {"status":False, "data":{"message":"???????? ?????????? ???? ???????? ??????????."}}
    problem_group = ProblemGroup.objects.filter(id=gid)[0]
    problems = problem_group.problems.all().select_subclasses()
    if len(problems) == 0:
        return {"status": False, "data":{"message":"???????? ?????????? ???????? ??????."}}
    submit = get_submit_from_group(gid, account)
    if submit is not None and submit['status'] != 'Received':
        return {"status": False, "data":{"message":"?????? ???????? ???? ?????? ???????? ?????????? ???????????? ???????? ?????? ?? ???????? ???? ???? ?????????????? ??????."}}
    if submit is not None:
        problem = Problem.objects.all().select_subclasses().filter(id=submit['problem'])[0]
        problem_data = ProblemSerializer(problem).data
        data = {}
        problem_data.pop('answer')
        data['problem'] = problem_data
        data['submit'] = submit
        return {"status": False, "data": data}
    return {"status":True, "problem": problems.order_by('?')[0]}

##  return status = True or False means get nre problem is ok
def get_problem_for_submit(pid, gid, account):
    if not ProblemGroup.objects.filter(id=gid).exists():
        return {"status":False, "data":{"message":"???????? ?????????? ???? ???????? ??????????."}}
    problem_group = ProblemGroup.objects.filter(id=gid)[0]
    problems = problem_group.problems.all().select_subclasses()
    if len(problems) == 0:
        return {"status": False, "data":{"message":"???????? ?????????? ???????? ??????."}}
    if len(problems.filter(id=pid)) == 0:
        return {"status": False, "data":{"message":"???????? ?????????? ???? ???? ?????? ???????? ???????? ??????????."}}
    submit = get_submit_from_problem(pid, account)
    if submit is not None and submit['status'] != 'Received':
        return {"status": False, "data":{"message":"?????? ???????? ???? ?????? ???????? ?????? ?????????? ???? ???????????? ???????? ?????? ?? ???????? ???? ???? ?????????????? ??????."}}
    if submit is not None:
        problem = Problem.objects.all().select_subclasses().filter(id=submit['problem'])[0]
        problem_data = ProblemSerializer(problem).data
        data = {}
        problem_data.pop('answer')
        data['problem'] = problem_data
        data['submit'] = submit
        return {"status": False, "data": data}
    return {"status":True, "problem": problems.get(id=pid)}


def is_problem_goten_from_group_view(account, gid):
    if get_submit_from_group(gid, account) is not None:
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

##  return responce with data
def request_problem_from_group_view(account, gid, game_problem_request_handler=None, game_problem_request_permission_chcker=None, pid=None):
    if pid is None:
        data = get_random_problem_from_group(gid, account)
    else:
        data = get_problem_for_submit(pid, gid, account)

    if not data["status"]:
        return Response(data["data"], status=status.HTTP_400_BAD_REQUEST)

    problem = data["problem"]
    if game_problem_request_permission_chcker is not None and\
        game_problem_request_permission_chcker(gid, account):
        return Response({"message":"???????? ?????????? ?????????? ?????????? ???? ????????????."}, status=status.HTTP_400_BAD_REQUEST)
    
    serializerClass = BaseSubmitSerializer.get_serializer(problem.problem_type)
    data = {}
    data['problem'] = problem.pk
    data['problem_group'] = gid
    data['respondents'] = []
    serializer = serializerClass(data=data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    instance = serializer.create(serializer.validated_data)
    instance.respondents.add(account)
    instance.save()
    if game_problem_request_handler is not None:
        game_problem_request_handler(account.user, instance)
    data = {}
    data['problem'] =  ProblemSerializer(problem).data
    data['submit'] = serializerClass(instance).data
    data['problem'].pop('answer')
    return Response(data, status=status.HTTP_200_OK)
    
def submit_answer_view(account, input_data, sid, pid, game_submit_handler=None):
    data = {}
    data['id'] = sid
    data['problem'] = pid
    if not Problem.objects.filter(id=pid).exists():
        return Response({"message":"?????????? ?????????? ????????!"},status=status.HTTP_400_BAD_REQUEST)
    problem = Problem.objects.filter(id=pid)[0]
    serializerClass = BaseSubmitSerializer.get_serializer(problem.problem_type)
    if not serializerClass.Meta.model.objects.filter(id=sid).exists():
        return Response({"message":"?????????? ???????? ???????? ?????????? ???? ???????????? ????????."},status=status.HTTP_400_BAD_REQUEST)
    instance = serializerClass.Meta.model.objects.filter(id=sid)[0]
    if len(instance.respondents.all().filter(id=account.id)) == 0:
        return Response({"message":"?????? ???????? ?????????? ???? ?????? ????????!"},status=status.HTTP_400_BAD_REQUEST)
    if instance.status != BaseSubmit.Status.Received:
        return Response({"message":"???????? ???????? ?????? ?????????? ???? ?????????? ???????? ??????!"},status=status.HTTP_400_BAD_REQUEST)
    
    if serializerClass == AutoCheckSubmitSerializer:
        data['answer'] = {}
        try:
            data['answer']['text'] = input_data['text']
        except:
            data['answer']['text'] = "???????? ???????? ??????????"
    else:
        data['text_answer'] = {}
        try:
            data['text_answer']['text'] = input_data['text']
        except:
            data['text_answer']['text'] = "???????? ???????? ??????????"
        data['upload_file_answer'] = {}
        try:
            data['upload_file_answer']['answer_file'] = input_data['file']
            data['upload_file_answer']['file_name'] = f'problem {pid} account {account.id}'
        except:
            data.pop('upload_file_answer')
    
    serializer = serializerClass(data=data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data
    instance = serializer.update(instance, data)
    if game_submit_handler is not None:
        game_submit_handler(instance, account.user, problem)
    response = serializer.to_representation(instance)
    return Response(response ,status=status.HTTP_200_OK)

def judge_view(account, sid , mark, game_judge_handler=None):
    submit = JudgeableSubmit.objects.filter(id=sid)[0]
    if submit.status == BaseSubmit.Status.Received:
        return Response({"message":"???????? ?????????? ???????? ?????? ?????????? ?????????? ???????? ??????."},status=status.HTTP_400_BAD_REQUEST)
    
    if submit.status == BaseSubmit.Status.Judged:
        return Response({"message":"?????? ?????????? ???????? ?????????? ?????? ??????."},status=status.HTTP_400_BAD_REQUEST)
    submit.judged_at = timezone.now()
    submit.status = BaseSubmit.Status.Judged
    submit.judged_by = account
    submit.mark = mark
    submit.save()
    if game_judge_handler is not None:
        game_judge_handler(submit)
    return Response(JudgeableSubmitSerializer(submit).data ,status=status.HTTP_200_OK)



@transaction.atomic
@api_view(['POST'])
@permission_classes([SubmitAnswerPermission])
def submit_answer_to_problem(request, gid, pid):
    response = request_problem_from_group_view(request.user.account, gid, pid=pid)

    if response.status_code != status.HTTP_200_OK:
        return response
    sid = response.data['submit']['id']
    data = {}
    try:
        data['text'] = request.data['text']
    except:
        pass
    try:
        data['file'] = request.FILES['file']
    except:
        pass
    return submit_answer_view(request.user.account, data, sid, pid)
    
@transaction.atomic
@api_view(['POST'])
@permission_classes([JudgePermission])
def judge_answer_view(request, pk , mark):
   return judge_view(request.user.account, pk, mark)

def get_judgeable_submits_by_remove_permissions(request, submits):
    out_list = []
    jp = JudgePermission()
    request.method = 'POST'
    for j in submits:
        request.parser_context['kwargs']['pk'] = j.pk
        if jp.has_permission(request, None):
            out_list.append(j.id)
    return JudgeableSubmit.objects.filter(id__in=out_list)


@api_view(['GET'])
def get_judgeable_submits(request):
    j_list = JudgeableSubmit.objects.all()
    j_list = get_judgeable_submits_by_remove_permissions(request, j_list)
    judgeable_submits_data = JudgeableSubmitSerializer(j_list, many=True).data
    return Response(judgeable_submits_data, status=status.HTTP_200_OK)