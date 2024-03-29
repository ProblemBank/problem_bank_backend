from problembank.models import BankAccount
from problembank.serializer import BankAccountSerializer
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
