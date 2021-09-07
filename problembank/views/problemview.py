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
from problembank.serializers import ProblemSerializer

import sys

class ProblemView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
    permission_classes = [permissions.AllowAny]
    queryset = Problem.objects.all().select_subclasses()
    serializer_class = ProblemSerializer

    @transaction.atomic
    def get_serializer_class(self):
        
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            try:
                return ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
                    self.request.data['problem_type']))
            except:
                pass
        # try:
        print(self.kwargs)
        instance = Problem.objects.filter(pk=self.kwargs['pk'])[0]
        print(getattr(sys.modules[__name__],\
                instance.problem_type))
        return ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
                instance.problem_type))
        # except: 
        #     print("!!!")