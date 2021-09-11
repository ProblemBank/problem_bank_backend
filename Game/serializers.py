from django.db.models import fields
from rest_framework import serializers

from .models import *


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
