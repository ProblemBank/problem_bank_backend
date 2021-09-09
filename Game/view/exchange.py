from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from Game.models import Exchange, Player, Merchandise
from Game.serializers import ExchangeSerializer
from django.db.models import Q


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_exchanges(request):
    exchanges = Exchange.objects.filter(buyer__isnull=True)
    exchanges_serializer = ExchangeSerializer(data=exchanges, many=True)
    exchanges_serializer.is_valid()
    return Response(exchanges_serializer.data, status=status.HTTP_200_OK)


class ExchangeView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ExchangeSerializer
    queryset = Exchange.objects.all()

    def get(self, request):
        user = request.user
        player = user.player_set.first()
        player_exchanges = self.get_queryset().filter(Q(seller=player) | Q(buyer=player)).order_by('-pk')
        player_exchanges_serializer = self.get_serializer(data=player_exchanges, many=True)
        player_exchanges_serializer.is_valid()
        return Response(player_exchanges_serializer.data, status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        player = user.player_set.first()
        exchange_id = request.data.get('exchange')
        print(exchange_id)
        exchange = self.get_queryset().filter(id=exchange_id).first()
        if not exchange:
            return Response({'message': 'این مزایده به فروش رفته است!'}, status.HTTP_404_NOT_FOUND)

        if not can_do_exchange(player, exchange):
            return Response({'message': 'دارایی شما برای انجام این مبادله کافی نیست!'}, status.HTTP_400_BAD_REQUEST)

        handle_exchange(exchange.seller, exchange.sold_merchandise, 'decrease')
        handle_exchange(exchange.seller, exchange.bought_merchandise, 'increase')
        handle_exchange(player, exchange.bought_merchandise, 'decrease')
        handle_exchange(player, exchange.sold_merchandise, 'increase')

        exchange.buyer = player
        exchange.save()

        return Response({'message': 'مبادله با موفقیت انجام شد!'}, status.HTTP_200_OK)


def can_do_exchange(player: Player, exchange: Exchange):
    bought_merchandise = exchange.bought_merchandise
    if player.coin >= bought_merchandise.coin and \
            player.black_toot >= bought_merchandise.black_toot and \
            player.blue_toot >= bought_merchandise.blue_toot and \
            player.red_toot >= bought_merchandise.red_toot:
        return True
    return False


def handle_exchange(player: Player, merchandise: Merchandise, type):
    tmp = 1
    if type == 'decrease':
        tmp = -1
    player.coin += tmp * merchandise.coin
    player.black_toot += tmp * merchandise.black_toot
    player.blue_toot += tmp * merchandise.blue_toot
    player.red_toot += tmp * merchandise.red_toot
    player.save()
