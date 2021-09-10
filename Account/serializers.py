from Game.models import Player
from problembank.models import BankAccount
from problembank.serializers import BankAccountSerializer, create_or_get_topic
from rest_framework import serializers
from .models import *
from django.db import transaction

# todo:
# TokenObtainPairSerializer

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        bank_account_data = {}
        bank_account_data['phone_number'] = validated_data['phone_number']
        bank_account_data['first_name'] = validated_data['first_name']
        bank_account_data['last_name'] = validated_data['last_name']
        bank_account_data['user'] = user
        BankAccount.objects.create(**bank_account_data)
        return user


class StudentSerializer(serializers.ModelSerializer):
    pass


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(max_length=250, required=True)
    new_password = serializers.CharField(max_length=250, required=True)

    def validated_password(self, value):
        validated_password(value)
        return value


class ResetPasswordSerializer(serializers.ModelSerializer):
    national_code = serializers.CharField(max_length=10)
    phone_number = serializers.CharField(max_length=15)
    new_password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['national_code', 'phone_number', 'new_password']

    def save(self):
        national_code = self.validated_data['national_code']
        phone_number = self.validated_data['phone_number']
        new_password = self.validated_data['new_password']

        if User.objects.filter(national_code=national_code).exists():
            user = User.objects.get(national_code=national_code)
            user.set_password(new_password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error': 'please enter valid crendentials'})

import csv
def add_accounts():
    with open('g4g.csv') as f:
        reader = csv.reader(f)

        for row in reader:
            try:
                data = {}
                data['password'] = row[0]
                data['username'] = row[4]
                data['first_name'] = row[2]
                data['last_name'] = row[3]
                data['phone_number'] = row[4]
                serializer = CreateUserSerializer(data=data)
                serializer.is_valid()
                data = serializer.validated_data
                user = serializer.create(data)
                user.save()
            except:
                pass
def get_team_data():
    team_data = []
    with open('g4g.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            username = row[4]
            team = row[1]
            team_data.append((team, username))
    team_data.sort()
    return team_data

def get_name_data():
    name_data = []
    with open('team.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            name_data.append((row[0], row[1]))
    name_data = dict(name_data)
    return name_data

def create_or_get_player(team, name_data, count):
    if len(Player.objects.filter(id=hash(team))) > 0:
        return Player.objects.filter(id=hash(team))[0]
    else:
        return Player.objects.create(name=name_data[team] if team in name_data else f'تیم شماره {count}', 
                                     coin=5000, id=hash(team))
    
def add_players():
    count = 100
    team_data = get_team_data()[2:]
    name_data = get_name_data()
    for mem in team_data:
        user = User.objects.filter(username=mem[1])[0]
        if len(Player.objects.filter(users__in=[user.id])) > 0:
            continue
        player = create_or_get_player(mem[0], name_data, count)
        player.users.add(user)
        player.save()
        count += 1
    