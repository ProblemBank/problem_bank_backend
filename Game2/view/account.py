from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction

from Game2.serializers import NotificationSerializer, TeamSerializer, RoomSerializer
from Game2.models import Notification, Team, Room, TeamRoom
from constants import MAX_ROOM_NUMBER, LAST_ROOM_COST


class StartGameView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    @transaction.atomic
    def get(self, request):
        user = request.user
        team = Team.objects.filter(users__in=[user])[0]
        # TODO Check problem_groups
        if len(TeamRoom.objects.filter(room__number=1, team=team)) == 0:
            first_room = Room.objects.create(number=1, )
            TeamRoom.objects.create(room=first_room, team=team)
        else:
            first_room = TeamRoom.objects.filter(room__number=1, team=team)[0].room
        team.current_room = first_room
        team.save()
        room_serializer = self.get_serializer(first_room)
        return Response(data=room_serializer.data, status=status.HTTP_200_OK)


class PreviousRoomView(generics.GenericAPIView):
    # TODO add previous page permissions
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    @transaction.atomic
    def get(self, request):
        user = request.user
        team = Team.objects.filter(users__in=[user])[0]
        current_room = team.current_room
        team_room = TeamRoom.objects.filter(room__number=current_room.number + 1, team=team)[0]
        prev_room = team_room.room
        team.current_room = prev_room
        team.save()
        room_serializer = self.get_serializer(prev_room)
        return Response(room_serializer.data, status.HTTP_200_OK)


class NextRoomView(generics.GenericAPIView):
    # TODO add permission to move to next page
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    @transaction.atomic
    def get(self, request):
        user = request.user
        team = Team.objects.filter(users__in=[user])[0]
        current_room = team.current_room
        entrance_cost = LAST_ROOM_COST if current_room.number + 1 == MAX_ROOM_NUMBER else 0

        if len(TeamRoom.objects.filter(room__number=(current_room.number + 1), team=team)) == 0:
            # TODO check problemGroups to add here
            next_room = Room.objects.create(number=current_room.number + 1, entrance_cost=entrance_cost)
            TeamRoom.objects.create(room=next_room, team=team)
        else:
            team_room = TeamRoom.objects.filter(room__number=current_room.number + 1, team=team)[0]
            next_room = team_room.room

        team.current_room = next_room
        next_room.save()
        team.save()
        room_serializer = self.get_serializer(next_room)
        return Response(room_serializer.data, status.HTTP_200_OK)


class TeamView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get(self, request):
        user = request.user
        team = self.queryset.filter(users__in=[user])[0]
        team_serializer = self.get_serializer(team)
        return Response(team_serializer.data, status.HTTP_200_OK)


class NotificationView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    @transaction.atomic
    def get(self, request):
        user = request.user
        user_notifications = self.get_queryset().filter(user=user, has_seen=False).order_by('-pk')[:10]
        user_notifications_serializer = self.get_serializer(data=user_notifications, many=True)
        user_notifications_serializer.is_valid()
        return Response(user_notifications_serializer.data, status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        notification_id = request.data.get('notification')
        notification = self.get_queryset().get(id=notification_id)
        notification.has_seen = True
        notification.save()
        return Response({}, status.HTTP_200_OK)
