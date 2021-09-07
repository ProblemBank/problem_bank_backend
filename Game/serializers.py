from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import *


# class ProblemSerializer(serializers.ModelSerializer):
#     problem = ProblemInfoSerializer()
#     from_auction = SerializerMethodField('is_problem_bought_from_auction')
#     auction_cost = SerializerMethodField('get_auction_cost')
#     is_sold = SerializerMethodField('is_problem_sold_in_auction')
#
#     def is_problem_bought_from_auction(self, answer):
#         auction = Auction.objects.filter(buyer=answer.player, problem=answer.problem)
#         if auction.exists():
#             return True
#         else:
#             return False
#
#     def is_problem_sold_in_auction(self, answer):
#         auction = Auction.objects.filter(seller=answer.player, problem=answer.problem)
#         if auction.exists():
#             return True
#         else:
#             return False
#
#     def get_auction_cost(self, answer):
#         auction = Auction.objects.filter(buyer=answer.player, problem=answer.problem).first()
#         return auction.price if auction else ''
#
#     class Meta:
#         model = Answer
#         fields = ['id', 'status', 'mark', 'problem', 'from_auction', 'is_sold', 'auction_cost']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PlayerSerializer(serializers.ModelSerializer):
    users = UserSerializer()

    class Meta:
        model = Player
        fields = ['name', 'users', 'score']
