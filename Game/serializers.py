from django.db.models import fields
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

class UserRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name']

class PlayerRewardSerializer(serializers.ModelSerializer):
    users = UserRewardSerializer(many=True)
    class Meta:
        model = Player
        fields = ['users', 'name', 'coin', 'blue_toot', 'red_toot', 'black_toot',
                  'fake_checkable_objects', 'not_fake_checkable_objects']

import csv
def convert_all():
    players = Player.objects.all()
    datas = []
    for player in players:
        data = PlayerRewardSerializer(player).data
        try:
            data['user1'] = data['users'][0]['user_name']
        except:
            pass
        try:
            data['user2'] = data['users'][1]['user_name']
        except:
            pass
        try:
            data['user3'] = data['users'][2]['user_name']
        except:
            pass
        data.pop('users')
        datas.append(data)
    file = open('data_file.csv', 'w')
    with file:
        header = ['user1', 'user2', 'user3', 'name', 'coin', 'blue_toot', 'red_toot', 'black_toot',
                  'fake_checkable_objects', 'not_fake_checkable_objects']
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        for i in range(0, len(datas)):
            writer.writerow(datas[i])

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PlayerSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Player
        fields = '__all__'


class MerchandiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = '__all__'


class CheckableObjectSerializer(serializers.ModelSerializer):
    merchandise = MerchandiseSerializer()

    class Meta:
        model = CheckableObject
        fields = '__all__'


class PrivateCheckableObjectSerializer(serializers.ModelSerializer):
    merchandise = MerchandiseSerializer()

    class Meta:
        model = CheckableObject
        exclude = ['is_fake']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        exclude = ['user']


class FamousPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamousPerson
        fields = '__all__'


class ExchangeSerializer(serializers.ModelSerializer):
    seller = PlayerSerializer()
    buyer = PlayerSerializer()
    sold_merchandise = MerchandiseSerializer()
    bought_merchandise = MerchandiseSerializer()

    class Meta:
        model = Exchange
        fields = '__all__'
