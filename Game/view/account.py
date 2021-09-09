from random import choice

from django.db.transaction import atomic
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from Game.models import Player, Notification
from Game.permissions import ReceiveProblem
from Game.serializers import PlayerSerializer, NotificationSerializer


class PlayerView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

    def get(self, request):
        user = request.user
        player = user.player_set.first()
        player_serializer = self.get_serializer(player)
        return Response(player_serializer.data, status.HTTP_200_OK)


class NotificationView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get(self, request):
        user = request.user
        user_notifications = self.get_queryset().filter(user=user, has_seen=False).order_by('-pk')[:10]
        user_notifications_serializer = self.get_serializer(data=user_notifications, many=True)
        user_notifications_serializer.is_valid()
        return Response(user_notifications_serializer.data, status.HTTP_200_OK)

    def post(self, request):
        notification_id = request.data.get('notification')
        notification = self.get_queryset().get(id=notification_id)
        notification.has_seen = True
        notification.save()
        return Response({}, status.HTTP_200_OK)


# class ScoreboardView(generics.GenericAPIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = PlayerSerializer
#     queryset = Player.objects.all()

#     def get(self, request):
#         players = Player.objects.filter().order_by('-score')
#         players_serializer = self.get_serializer(data=players, many=True)
#         players_serializer.is_valid()
#         return Response(players_serializer.data, status.HTTP_200_OK)
