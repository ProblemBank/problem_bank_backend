from random import choice

from django.db.transaction import atomic
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from Game.models import Player
from Game.permissions import ReceiveProblem
from Game.serializers import PlayerSerializer


class PlayerView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlayerSerializer

    def get(self, request):
        user = request.user
        player = user.player_set.filter().first()
        if player is None:
            return Response({"message": "بازیکنی یافت نشد"}, status.HTTP_404_NOT_FOUND)
        player_serializer = self.get_serializer(player)
        return Response(player_serializer.data, status.HTTP_200_OK)


class ScoreboardView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

    def get(self, request):
        players = Player.objects.filter().order_by('-score')
        players_serializer = self.get_serializer(data=players, many=True)
        players_serializer.is_valid()
        return Response(players_serializer.data, status.HTTP_200_OK)


def get_random(query_set):
    pks = query_set.values_list('pk', flat=True).order_by('id')
    random_pk = choice(pks)
    return query_set.get(pk=random_pk)


@atomic
def make_transaction(player: Player, value: int):
    player.score += value
    player.save()

    # new_transaction = Transaction()
    # new_transaction.player = player
    # new_transaction.title = title
    # new_transaction.amount = value
    #
    # new_transaction.save()
