from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from Game.models import Problem, Answer, BaseAnswer
from .serializers import AuctionSerializers
from .permissions import OpenAuctionsLimit, seller_answer_problem, DuplicateLimit, SameSellerAndBuyer, \
    AlreadyHaveProblem


class CreateAuctionProblem(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, OpenAuctionsLimit, DuplicateLimit]
    serializer_class = AuctionSerializers
    queryset = Auction.objects.filter(done_deal=False)

    def create(self, request, *args, **kwargs):
        user = request.user
        price = request.data.get('price')
        problem_id = request.data.get('problem')
        game_id = request.data.get('game')

        player_user = Player.objects.get(users__in=[user], game__id=game_id)
        problem = Problem.objects.get(id=problem_id)

        auction_obj = Auction(seller=player_user, problem=problem, price=price)
        auction_obj.save()
        return Response({"message": "مسئله با موفقیت در تابلوی مزایده قرار گرفت."}, status.HTTP_200_OK)


class BuyAuctionProblem(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, SameSellerAndBuyer, AlreadyHaveProblem]

    def post(self, request, game_id):
        auction_id = request.data['auction']
        user = request.user
        auction_obj = Auction.objects.get(id=auction_id)
        player_user = Player.objects.get(users__in=[user], game__id=game_id)

        auction_obj.done_deal = True
        auction_obj.buyer = player_user
        auction_obj.save()

        player_user.score -= auction_obj.price
        player_user.save()

        auction_obj.seller.score += auction_obj.price
        auction_obj.seller.save()

        new_problem = Answer(player=player_user, problem=auction_obj.problem)
        new_problem.save()

        return Response({"message": "خرید مسئله با موفقیت انجام شد."}, status.HTTP_200_OK)


class AllAuctionsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, game_id):
        all_auctions = Auction.objects.filter(seller__game__id=game_id)
        all_auctions_serializer = AuctionSerializers(data=all_auctions, many=True)
        all_auctions_serializer.is_valid()
        return Response(all_auctions_serializer.data, status.HTTP_200_OK)
