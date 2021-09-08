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
from problembank.serializers import ProblemSerializer, DescriptiveProblemSerializer, ShortAnswerProblemSerializer, ShortAnswerProblemSerializer
from django.utils import timezone
import sys

class ProblemView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Problem.objects.all().select_subclasses()
    serializer_class = ProblemSerializer

    @transaction.atomic
    def get_serializer_class(self):
        print(self.request.user, self.request.method)
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            try:
                return ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
                    self.request.data['problem_type']))
            except Exception as e:
                print(e)
        instance = Problem.objects.filter(pk=self.kwargs['pk'])[0]
        return ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
                instance.problem_type))

    # @transaction.atomic
    # def create(self, request, *args, **kwargs):
    #     return super(ProblemView, self).create(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        data['is_checked'] = 'False'
        serializerClass = self.get_serializer_class()
        serializer = serializerClass(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data['author'] = request.user.account
        instance = serializer.create(data)
        instance.save()

        response = serializer.to_representation(instance)
        return Response(response)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_problems(request):
    problems = Problem.objects.all()
    problems_data = ProblemSerializer(problems.select_subclasses(), many=True).data
    return Response(problems_data, status=status.HTTP_200_OK)
     