from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from problembank.serializers.event_serializer import ShortEventSerializer

from problembank.models import *
from rest_framework import permissions
# from problembank.views import permissions as customPermissions
from problembank.serializers.event_serializer import EventSerializer
from problembank.permissions import DefaultPermission, EventPermission
import sys


class EventView(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated, customPermissions.MentorPermission, ]
    permission_classes = [permissions.IsAuthenticated, EventPermission]
    queryset = Event.objects.all()
    serializer_class = ShortEventSerializer

    def get_serializer_context(self):
        context = super(EventView, self).get_serializer_context()
        context.update({"request": self.request})
        return context


@api_view(['GET'])
@permission_classes([EventPermission])
@transaction.atomic
def get_event(request, pk):
    serializer = ShortEventSerializer(data={'id': pk})
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_events(request):
    user = request.user
    events = Event.objects.all()
    my_events: bool = request.data.get('my_events', False)
    if my_events:
        events = events.filter(Q(mentors__in=[user.account]) | Q(
            participants__in=[user.account])).distinct()
    name_prefix: str = request.data.get('name_prefix', None)
    if name_prefix:
        events = events.filter(title__startswith=name_prefix)
    serializer = ShortEventSerializer(
        data=events, many=True, context={'request': request})
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_event(request, pk):
    account = request.user.account
    event = Event.objects.get(pk=pk)
    if not event:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not 'password' in request.data:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    password = request.data['password']
    if password == event.mentor_password:
        event.mentors.add(account)
        return Response(status=status.HTTP_200_OK)
    elif password == event.participant_password:
        event.participants.add(account)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
