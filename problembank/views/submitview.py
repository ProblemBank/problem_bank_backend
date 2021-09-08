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

class JudgeableSubmitView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JudgeableSubmitSerializer
    queryset = JudgeableSubmit.objects.all()


class AutoCheckSubmitView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    queryset = AutoCheckSubmit.objects.all()
    serializer_class = AutoCheckSubmitSerializer



def get_random_problem_from_group(gid, account):
    try:
        problem_group = ProblemGroup.objects.filter(id=gid)[0]
    except:
        return Response("چنین گروه مسئله ای وجود ندارد.",status=status.HTTP_400_BAD_REQUEST)

    problems = problem_group.problems.all().select_subclasses()
    if len(AutoCheckSubmit.objects.all().select_subclasses().filter(problem_group=gid, respondents__in=[account])) > 0:
        return Response("شما قبلا از این دسته مسئله دریافت کرده اید.",status=status.HTTP_400_BAD_REQUEST)
    if len(JudgeableSubmit.objects.all().select_subclasses().filter(problem_group=gid, respondents__in=[account])) > 0:
        return Response("شما قبلا از این دسته مسئله دریافت کرده اید.",status=status.HTTP_400_BAD_REQUEST)
    
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
    pass
