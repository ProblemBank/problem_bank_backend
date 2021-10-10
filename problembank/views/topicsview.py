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
from problembank.permissions import DefualtPermission, SourcePermission, SubtopicPermission, TopicPermission
# from problembank.views import permissions as customPermissions
from problembank.serializers import SourceSerializer, SubtopicSerializer, TopicSerializer

import sys

class TopicView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
    permission_classes = [permissions.IsAuthenticated, TopicPermission]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class SubtopicView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
    permission_classes = [permissions.IsAuthenticated, SubtopicPermission]
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer


class SourceView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
    permission_classes = [permissions.IsAuthenticated, SourcePermission]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

   