from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from Game.models import Exchange, Player, Merchandise
from Game.serializers import ExchangeSerializer, MerchandiseSerializer
from django.db.models import Q


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_all_exchanges(request):
    exchanges = Exchange.objects.filter(buyer__isnull=True)
    valid_exchange = []
    for exchange in exchanges:
        if does_seller_have_enough_commodity(exchange.seller, exchange.sold_merchandise):
            valid_exchange.append(exchange)

    exchanges_serializer = ExchangeSerializer(data=valid_exchange, many=True)
    exchanges_serializer.is_valid()
    return Response(exchanges_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_new_exchange(request):
    user = request.user
    player = user.player_set.first()

    sold_merchandise = request.data.get('sold_merchandise')
    bought_merchandise = request.data.get('bought_merchandise')

    sold_merchandise_serializer = MerchandiseSerializer(data=sold_merchandise)
    bought_merchandise_serializer = MerchandiseSerializer(data=bought_merchandise)

    if not sold_merchandise_serializer.is_valid() or not bought_merchandise_serializer.is_valid():
        return Response({"message": "اطلاعات ورودی کالا اشتباه است!"}, status=status.HTTP_400_BAD_REQUEST)

    sold_merchandise = sold_merchandise_serializer.create(sold_merchandise_serializer.validated_data)
    bought_merchandise = bought_merchandise_serializer.create(bought_merchandise_serializer.validated_data)

    if not does_seller_have_enough_commodity(player, sold_merchandise):
        return Response({"message": "دارایی شما برای ایجاد همچین مبادله‌ای کافی نیست!"},
                        status=status.HTTP_400_BAD_REQUEST)

    Exchange(seller=player, sold_merchandise=sold_merchandise, bought_merchandise=bought_merchandise).save()

    return Response({"message": "مبادله با موفقیت ساخته شد!"}, status=status.HTTP_200_OK)


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

        if not does_seller_have_enough_commodity(exchange.seller, exchange.sold_merchandise):
            return Response({'message': 'منابع فروشنده در این لحظه برای انجام مبادله کافی نیست!'},
                            status.HTTP_400_BAD_REQUEST)

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


def does_seller_have_enough_commodity(seller: Player, sold_merchandise: Merchandise):
    if seller.coin >= sold_merchandise.coin and \
            seller.black_toot >= sold_merchandise.black_toot and \
            seller.blue_toot >= sold_merchandise.blue_toot and \
            seller.red_toot >= sold_merchandise.red_toot:
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
