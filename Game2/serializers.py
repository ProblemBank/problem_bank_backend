from rest_framework import serializers
from django.db import transaction

from .models import Team, Notification, Room, TeamRoom
from Account.models import User
from problembank.models import BankAccount
from constants import MAX_ROOM_NUMBER, LAST_ROOM_COST


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save()
        bank_account_data = {
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'user': user,
        }
        BankAccount.objects.create(bank_account_data)
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
        fields = ['name', 'coin', 'carrousel_turn', 'leader']

    @transaction.atomic
    def create(self, validated_data):
        team = Team.objects.create(**validated_data)
        team.save()
        for i in range(1, MAX_ROOM_NUMBER + 1):
            entrance_cost = LAST_ROOM_COST if i == MAX_ROOM_NUMBER else 0
            # todo add problemGroups here!
            room = Room.objects.create(number=i, entrance_cost=entrance_cost)
            TeamRoom.objects.create(room=room, team=team)
        return team
