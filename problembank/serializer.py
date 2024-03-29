from django.db.models import base
from django.http.response import ResponseHeaders
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import sys
from .models import *
from django.db import transaction
import json
from problembank.serializers.problem_group_serializer import ProblemGroupSerializerWithoutProblems


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = '__all__'


class ShortAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswer
        fields = '__all__'


class DescriptiveAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptiveAnswer
        fields = '__all__'


class UploadFileAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileAnswer
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    @classmethod
    def get_serializer(cls, model):
        if model == ShortAnswer:
            return ShortAnswerSerializer
        elif model == DescriptiveAnswer:
            return DescriptiveAnswerSerializer
        elif model == UploadFileAnswer:
            return UploadFileAnswerSerializer

    def to_representation(self, instance):
        serializer = AnswerSerializer.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):
        serializerClass = AnswerSerializer.get_serializer(getattr(sys.modules[__name__],
                                                                  validated_data['answer_type']))
        serializer = serializerClass(validated_data)
        return serializer.create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        serializerClass = AnswerSerializer.get_serializer(getattr(sys.modules[__name__],
                                                                  validated_data['answer_type']))
        serializer = serializerClass(validated_data)
        return serializer.update(instance, validated_data)


class ShortAnswerProblemSerializer(serializers.ModelSerializer):
    answer = ShortAnswerSerializer()
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = ShortAnswerProblem
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True},
                        'publish_date': {'read_only': True},
                        'last_change_date': {'read_only': True},
                        'upvote_count': {'read_only': True},
                        }

    @transaction.atomic
    def create(self, validated_data):
        topics_data = validated_data.pop('topics')
        subtopics_data = validated_data.pop('subtopics')
        answer_data = validated_data.pop('answer')
        answer_data['answer_type'] = 'ShortAnswer'
        answer = ShortAnswer.objects.create(**answer_data)
        validated_data['answer'] = answer
        instance = ShortAnswerProblem.objects.create(**validated_data)
        instance.topics.set(topics_data)
        instance.subtopics.set(subtopics_data)
        instance.answer = answer
        instance.publish_date = timezone.now()
        instance.last_change_date = timezone.now()
        instance.upvote_count = 0
        instance.save()

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        ShortAnswer.objects.filter(id=instance.answer.id).update(
            **validated_data.pop('answer'))
        answer = ShortAnswer.objects.filter(id=instance.answer.id)[0]
        answer.answer_type = 'ShortAnswer'
        answer.save()
        instance.answer = answer
        instance.topics.set(validated_data.pop('topics'))
        instance.subtopics.set(validated_data.pop('subtopics'))
        instance.save()
        ShortAnswerProblem.objects.filter(
            id=instance.id).update(**validated_data)
        instance = ShortAnswerProblem.objects.filter(id=instance.id)[0]
        instance.last_change_date = timezone.now()
        instance.save()
        return instance


class DescriptiveProblemSerializer(serializers.ModelSerializer):
    answer = DescriptiveAnswerSerializer(required=False)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = DescriptiveProblem
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True},
                        'publish_date': {'read_only': True},
                        'last_change_date': {'read_only': True},
                        'upvote_count': {'read_only': True},
                        }

    @transaction.atomic
    def create(self, validated_data):
        topics_data = validated_data.pop('topics')
        subtopics_data = validated_data.pop('subtopics')
        answer_data = validated_data.pop('answer')
        answer_data['answer_type'] = 'DescriptiveAnswer'
        answer = DescriptiveAnswer.objects.create(**answer_data)
        validated_data['answer'] = answer
        instance = DescriptiveProblem.objects.create(**validated_data)
        instance.topics.set(topics_data)
        instance.subtopics.set(subtopics_data)
        instance.answer = answer
        instance.publish_date = timezone.now()
        instance.last_change_date = timezone.now()
        instance.upvote_count = 0
        instance.is_checked = False
        instance.save()

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        DescriptiveAnswer.objects.filter(id=instance.answer.id).update(
            **validated_data.pop('answer'))
        answer = DescriptiveAnswer.objects.filter(id=instance.answer.id)[0]
        answer.answer_type = 'DescriptiveAnswer'
        answer.save()
        instance.answer = answer
        instance.topics.set(validated_data.pop('topics'))
        instance.subtopics.set(validated_data.pop('subtopics'))
        instance.save()
        DescriptiveProblem.objects.filter(
            id=instance.id).update(**validated_data)
        instance = DescriptiveProblem.objects.filter(id=instance.id)[0]
        instance.last_change_date = timezone.now()
        instance.save()
        return instance


class ProblemSerializer(serializers.ModelSerializer):
    @classmethod
    def get_serializer(cls, model):
        if model == ShortAnswerProblem:
            return ShortAnswerProblemSerializer
        elif model == DescriptiveProblem:
            return DescriptiveProblemSerializer

    @transaction.atomic
    def create(self, validated_data):
        serializerClass = ProblemSerializer.get_serializer(getattr(sys.modules[__name__],
                                                                   validated_data['problem_type']))
        serializer = serializerClass(validated_data)

        return serializer.create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        serializerClass = ProblemSerializer.get_serializer(getattr(sys.modules[__name__],
                                                                   validated_data['problem_type']))
        serializer = serializerClass(validated_data)

        return serializer.update(instance, validated_data)

    def to_representation(self, instance):
        serializer = ProblemSerializer.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data

    # @classmethod
    # def get_problem_data(instance):
    #     getattr(sys.modules[__name__], self.request.data['problem_type'])
    #     serializer = ProblemSerializer.get_serializer(instance.__class__)
    #     return serializer(instance, context=self.context).data


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class PublicBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        exclude = ['phone_number', 'email', 'user']


class ProblemGroupSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, required=False)

    class Meta:
        model = ProblemGroup
        fields = '__all__'

    def create(self, validated_data):
        problems_data = validated_data.pop('problems')

        instance = ProblemGroup.objects.create(**validated_data)
        instance.problems.set(problems_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.problems.set(validated_data.pop('problems'))
        instance.save()
        ProblemGroup.objects.filter(id=instance.id).update(**validated_data)
        instance = ProblemGroup.objects.filter(id=instance.id)[0]
        return instance

    def to_representation(self, instance):
        problems_data = ProblemSerializer(
            instance.problems.select_subclasses(), context=self.context, many=True).data
        data = ProblemGroupSerializerWithoutProblems(
            instance, context=self.context).data
        data['problems'] = problems_data
        return data


class AutoCheckSubmitSerializer(serializers.ModelSerializer):
    answer = ShortAnswerSerializer(required=False)

    class Meta:
        model = AutoCheckSubmit
        fields = '__all__'
        extra_kwargs = {'status': {'read_only': True},
                        'received_at': {'read_only': True},
                        'delivered_at': {'read_only': True},
                        'judged_at': {'read_only': True},
                        'respondents': {'read_only': True},
                        }

    @transaction.atomic
    def create(self, validated_data):
        try:
            answer_data = validated_data.pop('answer')
        except:
            pass
        answer_data = {}
        answer_data['text'] = "بدون پاسخ"
        answer_data['answer_type'] = 'ShortAnswer'
        answer = ShortAnswer.objects.create(**answer_data)

        instance = AutoCheckSubmit.objects.create(**validated_data)
        instance.answer = answer
        instance.received_at = timezone.now()
        instance.mark = 0
        instance.status = BaseSubmit.Status.Received
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        ShortAnswer.objects.filter(id=instance.answer.id).update(
            **validated_data.pop('answer'))
        answer = ShortAnswer.objects.filter(id=instance.answer.id)[0]
        answer.answer_type = 'ShortAnswer'
        answer.save()
        instance.answer = answer
        instance.save()
        AutoCheckSubmit.objects.filter(id=instance.id).update(**validated_data)
        instance = AutoCheckSubmit.objects.filter(id=instance.id)[0]

        instance.delivered_at = timezone.now()
        instance.mark = 0
        instance.status = BaseSubmit.Status.Delivered

        instance.judged_at = timezone.now()
        problem = Problem.objects.all().select_subclasses().filter(
            id=instance.problem.id)[0]
        if problem.answer.text == instance.answer.text:
            instance.mark = 1
        else:
            instance.mark = 0
        instance.status = BaseSubmit.Status.Judged

        instance.save()
        return instance


class JudgeableSubmitSerializer(serializers.ModelSerializer):
    text_answer = DescriptiveAnswerSerializer(required=False)
    upload_file_answer = UploadFileAnswerSerializer(required=False)

    class Meta:
        model = JudgeableSubmit
        fields = '__all__'
        extra_kwargs = {'status': {'read_only': True},
                        'received_at': {'read_only': True},
                        'delivered_at': {'read_only': True},
                        'judged_at': {'read_only': True},
                        'judged_by': {'read_only': True},
                        'respondents': {'read_only': True},
                        }

    @transaction.atomic
    def create(self, validated_data):
        try:
            text_answer_data = validated_data.pop('text_answer')
        except:
            pass
        text_answer_data = {}
        text_answer_data['text'] = "بدون پاسخ"
        text_answer_data['answer_type'] = 'DescriptiveAnswer'
        text_answer = DescriptiveAnswer.objects.create(**text_answer_data)

        try:
            validated_data.pop('upload_file_answer')
        except:
            pass

        instance = JudgeableSubmit.objects.create(**validated_data)
        instance.text_answer = text_answer
        instance.received_at = timezone.now()
        instance.mark = 0
        instance.status = BaseSubmit.Status.Received
        instance.save()
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        DescriptiveAnswer.objects.filter(id=instance.text_answer.id).update(
            **validated_data.pop('text_answer'))
        text_answer = DescriptiveAnswer.objects.filter(
            id=instance.text_answer.id)[0]
        text_answer.answer_type = 'DescriptiveAnswer'
        text_answer.save()
        instance.text_answer = text_answer
        try:
            upload_file_answer_data = validated_data.pop('upload_file_answer')
            upload_file_answer_data['answer_type'] = 'UploadFileAnswer'
            upload_file_answer = UploadFileAnswer.objects.create(
                **upload_file_answer_data)
            instance.upload_file_answer = upload_file_answer
        except:
            pass

        instance.save()
        JudgeableSubmit.objects.filter(id=instance.id).update(**validated_data)
        instance = JudgeableSubmit.objects.filter(id=instance.id)[0]

        instance.delivered_at = timezone.now()
        instance.mark = 0
        instance.status = BaseSubmit.Status.Delivered

        instance.save()
        return instance


class BaseSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSubmit
        fields = '__all__'

    @classmethod
    def get_serializer(cls, problem_type):
        if problem_type == 'ShortAnswerProblem':
            return AutoCheckSubmitSerializer
        else:
            return JudgeableSubmitSerializer

    def to_representation(self, instance):
        serializer = BaseSubmitSerializer.get_serializer(
            instance.problem.problem_type)
        return serializer(instance, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):
        serializerClass = BaseSubmitSerializer.get_serializer(
            validated_data['problem'].problem_type)
        serializer = serializerClass(validated_data)
        return serializer.create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        serializerClass = BaseSubmitSerializer.get_serializer(
            instance.problem.problem_type)
        serializer = serializerClass(validated_data)
        return serializer.update(instance, validated_data)


class GuidanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guidance
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class FilterSerializer(serializers.Serializer):
    subtopics = serializers.ListField(child=serializers.IntegerField())
    topics = serializers.ListField(child=serializers.IntegerField())
    sources = serializers.ListField(child=serializers.IntegerField())
    grades = serializers.ListField(child=serializers.CharField())
    difficulties = serializers.ListField(child=serializers.CharField())
    page = serializers.IntegerField(default=1)
