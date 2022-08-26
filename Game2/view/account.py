from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone

from Game2.serializers import NotificationSerializer, TeamSerializer, RoomSerializer
from Game2.models import Notification, Team, Room, TeamRoom, GameInfo
from constants import MAX_ROOM_NUMBER, LAST_ROOM_COST


class RoomView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = RoomSerializer
    queryset = TeamRoom.objects.all()

    @transaction.atomic()
    def send_changed_room_notification(self, r_name, message, team):
        data = {
            'title': f'شما به اتاق {r_name} منتقل شدید!',
            'body': message,
            'user': team,
            'time': timezone.now()
        }
        Notification.objects.create(**data)

    @transaction.atomic
    def get(self, request, r_name):
        user = request.user
        team = Team.objects.filter(users__in=[user])[0]
        dest_room = self.queryset.filter(team=team, room__name=r_name)[0].room
        entrance_cost = dest_room.entrance_cost
        team.coin -= entrance_cost
        team.current_room = dest_room
        team.save()
        room_serializer = self.get_serializer(dest_room)
        room_serializer.is_valid()
        self.send_changed_room_notification(r_name, request.message, team)
        return Response(data=room_serializer.data, status=status.HTTP_200_OK)


class TeamView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get(self, request):
        user = request.user
        team = self.queryset.filter(users__in=[user]).first()
        team_serializer = self.get_serializer(team)
        # TODO Check this part!!
        team_serializer.data['finish_time'] = GameInfo.objects.get(
            pk=1).finish_time
        return Response(team_serializer.data, status.HTTP_200_OK)


class NotificationView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    @transaction.atomic
    def get(self, request):
        user = request.user
        team = Team.objects.filter(users__in=[user]).first()
        user_notifications = self.get_queryset().filter(
            team=team, has_seen=False).order_by('-pk')[:10]
        user_notifications_serializer = self.get_serializer(
            data=user_notifications, many=True)
        user_notifications_serializer.is_valid()
        return Response(user_notifications_serializer.data, status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        notification_id = request.data.get('notification')
        notification = self.get_queryset().get(id=notification_id)
        notification.has_seen = True
        notification.save()
        return Response({}, status.HTTP_200_OK)
