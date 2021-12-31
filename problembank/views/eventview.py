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



def get_events_by_remove_permissions(request, events):
    out_list = []
    event_permission = EventPermission()
    request.method = 'GET'
    for event in events:
        request.parser_context['kwargs']['pk'] = event.pk
        if event_permission.has_permission(request, None):
            out_list.append(event.id)
    return Event.objects.filter(id__in=out_list)


def get_minimal_event_data(event_pk, account_id):
    event = Event.objects.get(id=event_pk)
    data = EventSerializer(event).data
    data.pop("mentors")
    data.pop("participants")
    data.pop("owner")
    if len(event.mentors.all().filter(id=account_id)) > 0:
        role = "mentor"
    elif len(event.participants.all().filter(id=account_id)) > 0:
        role = "participant"
    elif event.owner.id == account_id:
        role = "owner"
    else:
        role = "anonymouse"
        
    if event.id == 7: #karsoogh 1401
        role = "mentor"

    data['role'] = role
    return data

@api_view(['GET'])
@permission_classes([EventPermission])
@transaction.atomic
def get_event(request, pk):
    data = get_minimal_event_data(pk, request.user.account.id)
    return Response(data=data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_events(request):
    event_list = Problem.objects.all()
    event_list = get_events_by_remove_permissions(request, event_list)
    events_data = []
    for event in event_list:
        events_data.append(get_minimal_event_data(event.pk, request.user.account.id))
    
    data = {'events':events_data}
    return Response(data, status=status.HTTP_200_OK)