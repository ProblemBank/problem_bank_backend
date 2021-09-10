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
from django.utils import timezone
import sys
from itertools import chain
# data['juged_by'] = request.user.account #just for mentor not all the times!
from problembank.permissions import DefualtPermission
class JudgeableSubmitView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = []
    serializer_class = JudgeableSubmitSerializer
    queryset = JudgeableSubmit.objects.filter(status=BaseSubmit.Status.Delivered)


class AutoCheckSubmitView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticated, DefualtPermission]
    queryset = AutoCheckSubmit.objects.all()
    serializer_class = AutoCheckSubmitSerializer



def get_random_problem_from_group(gid, account):
    try:
        problem_group = ProblemGroup.objects.filter(id=gid)[0]
    except:
        return Response("چنین گروه مسئله ای وجود ندارد.",status=status.HTTP_400_BAD_REQUEST)

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
        if submit['status'] == 'Delivered':
            return Response("شما قبلا از اینجا مسئله دریافت کرده اید و پاسخ آن را فرستاده اید.",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(submit,status=status.HTTP_400_BAD_REQUEST)
    try:
        return problems.order_by('?')[0]
    except:
        return Response("گروه مسئله خالی است.",status=status.HTTP_400_BAD_REQUEST)

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
    instance.respondents.add(account) #add other players
    instance.save()
    return Response(ProblemSerializer(problem).data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_answer(request):
    data = request.data
    problem = Problem.objects.filter(id=data['problem'])[0]
    serializerClass = BaseSubmitSerializer.get_serializer(problem.problem_type)
    instance = serializerClass.Meta.model.objects.filter(id=data['id'])[0]
    serializer = serializerClass(data=data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    data = serializer.validated_data
    instance = serializer.update(instance, data)
    instance.save()

    response = serializer.to_representation(instance)
    return Response(response ,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, DefualtPermission])
def judge(request, pid , mark):
    account = request.user.account
    submit = JudgeableSubmit.objects.filter(id=pid)[0]
    submit.judged_at = timezone.now()
    submit.status = BaseSubmit.Status.Judged
    submit.judged_by = account
    submit.mark = mark
    submit.save()
    return Response(JudgeableSubmitSerializer(submit).data ,status=status.HTTP_200_OK)

# instance.judged_at = timezone.now()
# instance.status = BaseSubmit.Status.Judged
# instance.judged_by = ??
