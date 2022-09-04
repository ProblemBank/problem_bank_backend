from django.db.models import base
from django.http.response import ResponseHeaders
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import sys
from problembank.models import *
from django.db import transaction
import json


class ShortEventSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        user = self.context['request'].user
        if obj.owner == user.account:
            role = "owner"
        elif obj.filter(mentors__in=[user.account]):
            role = "mentor"
        elif obj.filter(participants=[user.account]):
            role = "participant"
        else:
            role = "anonymous"
        return role

    class Meta:
        model = Event
        fields = ['id', 'image_link', 'problem_groups', 'role', 'title']
