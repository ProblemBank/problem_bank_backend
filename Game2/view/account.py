from rest_framework import generics, permissions, status
from rest_framework.response import Response

from Game2.serializers import NotificationSerializer, TeamSerializer
from Game2.models import Notification, Team


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

