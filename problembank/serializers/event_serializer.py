from rest_framework import serializers
from problembank.models import Event
from .problem_group_serializer import ProblemGroupSerializerWithoutProblems


class EventSerializer(serializers.ModelSerializer):
    problem_groups = ProblemGroupSerializerWithoutProblems(
        many=True, required=False)

    class Meta:
        model = Event
        exclude = ['mentor_password', 'participant_password']
        extra_kwargs = {'owner': {'read_only': True}}

    def update(self, instance, validated_data):
        instance.mentors.set(validated_data.pop('mentors'))
        instance.participants.set(validated_data.pop('participants'))
        instance.save()
        Event.objects.filter(id=instance.id).update(**validated_data)
        instance = Event.objects.filter(id=instance.id)[0]
        return instance


class ShortEventSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    problem_groups = ProblemGroupSerializerWithoutProblems(
        many=True, required=False)

    def create(self, validated_data):
        user = self.context.get('request').user
        new_event = Event.objects.create(**validated_data)
        new_event.mentors.add(user.account)
        new_event.owner = user.account
        new_event.save()
        return new_event

    def get_role(self, obj):
        user = self.context['request'].user
        if obj.owner == user.account:
            role = "owner"
        elif user.account in obj.mentors.all():
            role = "mentor"
        elif user.account in obj.participants.all():
            role = "participant"
        else:
            role = "anonymous"
        return role

    class Meta:
        model = Event
        fields = ['id', 'image_link', 'problem_groups', 'role', 'title']
