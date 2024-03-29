from rest_framework import serializers
from django.db import transaction

from .models import Team, Notification, Room, TeamRoom, Box, TeamBox, GameInfo
from Account.models import User
from problembank.models import BankAccount


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        # print(validated_data)
        user = User.objects.create(**validated_data)
        user.save()
        bank_account_data = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
        }
        BankAccount.objects.create(**bank_account_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'lastname']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        team = Team.objects.create(**validated_data)
        for i in range(1, GameInfo.objects.get(id=1).max_room_number + 1):
            entrance_cost = GameInfo.objects.get(id=1).last_room_cost if i == GameInfo.objects.get(id=1).\
                max_room_number else 0
            # todo add problemGroups here!
            room = Room.objects.create(
                name=str(i), entrance_cost=entrance_cost)
            TeamRoom.objects.create(room=room, team=team)
        return team


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'


class TeamBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamBox
        fields = '__all__'
