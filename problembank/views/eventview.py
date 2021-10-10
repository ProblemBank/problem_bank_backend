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
from problembank.serializers import EventSerializer
from problembank.permissions import DefualtPermission, EventPermission
import sys

class EventView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
    permission_classes = [permissions.IsAuthenticated, EventPermission]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        serializerClass = self.get_serializer_class()
        serializer = serializerClass(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        data['owner'] = request.user.account
        instance = serializer.create(data)
        instance.save()

        response = serializer.to_representation(instance)
        return Response(response)
