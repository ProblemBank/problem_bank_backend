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

# class SubmitView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
#                    mixins.UpdateModelMixin):
#     #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = BaseSubmit
#     queryset = list(chain(JudgeableSubmit.objects.all(), AutoCheckSubmit.objects.all()))

#     @transaction.atomic
#     def get_serializer_class(self):
#         print(self.request.user, self.request.method)
#         if self.request.method == 'POST' or self.request.method == 'PATCH':
#             try:
#                 return BaseSubmitSerializer.get_serializer(self.request.data['problem_type'])
#             except Exception as e:
#                 print(e)
#         instance = BaseSubmit.objects.filter(pk=self.kwargs['pk'])[0]
#         return BaseSubmitSerializer.get_serializer(instance.problem_type)

#     # @transaction.atomic
#     # def create(self, request, *args, **kwargs):
#     #     return super(ProblemView, self).create(request, *args, **kwargs)

#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serializerClass = self.get_serializer_class()
#         serializer = serializerClass(data=data)
#         if not serializer.is_valid(raise_exception=True):
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         data = serializer.validated_data
#         instance = serializer.create(data)
#         instance.save()
#         response = serializer.to_representation(instance)
#         return Response(response)
