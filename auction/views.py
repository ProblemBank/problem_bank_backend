from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from Game.models import Problem, ProblemAnswer, BaseAnswer
from .serializers import AuctionSerializers
from .permissions import problem_sell_limit, seller_answer_problem


class CreateAuctionProblem(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, problem_sell_limit]
    serializer_class = AuctionSerializers
    queryset = Auction.objects.filter(done_deal=False)

    def perform_create(self, serializer):
        auction_obj = serializer.save()

        player_user = Player.objects.get(user=self.request.user)
        problem = Problem.objects.get(id=self.request.data.get('problem_id'))
        auction_obj.player = player_user
        auction_obj.problem_for_sell = problem
        auction_obj.save()


class BuyAuctionProblem(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auction_obj = Auction.objects.get(id=request.data.get('auction_id'))
        player_user = Player.objects.get(user=self.request.user)
        if auction_obj.problem_for_sell.id != player_user.id:
            auction_obj.done_deal = True
            player_user.score -= auction_obj.price
            player_user.save()
            new_player_problem = PlayerSingleProblem(player=player_user, problem=auction_obj.problem_for_sell)
            new_player_problem.save()
            auction_obj.save()
            return Response({"message": "خرید با موفقیت انجام شد"}, status.HTTP_200_OK)

        else:
            return Response({"message": "شما نمی توانید سوالی که به مزایده گذاشتید را نمی توانید بخرید!"}, status.HTTP_403_FORBIDDEN)