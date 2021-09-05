from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import sys
from .models import *
from django.db import transaction


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
        serializerClass = AnswerSerializer.get_serializer(getattr(sys.modules[__name__],\
            validated_data['type']))
        serializer = serializerClass(validated_data)
        return serializer.create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        serializerClass = AnswerSerializer.get_serializer(getattr(sys.modules[__name__],\
            validated_data['type']))
        serializer = serializerClass(validated_data)
        return serializer.update(instance, validated_data)


class ShortAnswerProblemSerializer(serializers.ModelSerializer):
    answer = ShortAnswerSerializer()

    class Meta:
        model = ShortAnswerProblem
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        answer_data = validated_data.pop('answer')
        instance = ShortAnswerProblem.objects.create(**validated_data)
        answer_data['type'] = 'ShortAnswer'
        answer = ShortAnswer.objects.create(**answer_data)
        answer.problem = instance
        answer.save()
    
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['pk'] = instance.pk
        try:
            answer = ShortAnswerProblem.objects.filter(problem=instance)[0]
            validated_data['answer']['pk'] = answer.pk
            answer.delete()
        except:
            pass
        instance.delete()
        instance = self.create(validated_data)
        return instance


class DescriptiveProblemSerializer(serializers.ModelSerializer):
    answer = DescriptiveAnswerSerializer()
    class Meta:
        model = DescriptiveProblem
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        answer_data = validated_data.pop('answer')
        instance = DescriptiveProblem.objects.create(**validated_data)
        answer_data['type'] = 'DescriptiveAnswer'
        answer = DescriptiveAnswer.objects.create(**answer_data)
        answer.problem = instance
        answer.save()
    
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['pk'] = instance.pk
        try:
            answer = DescriptiveAnswer.objects.filter(problem=instance)[0]
            validated_data['answer']['pk'] = answer.pk
            answer.delete()
        except:
            pass
        instance.delete()
        instance = self.create(validated_data)
        return instance


class BaseProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProblem
        fields = '__all__'



class ProblemSerializer(serializers.ModelSerializer):
    base_problem = BaseProblemSerializer()
    @classmethod
    def get_serializer(cls, model):
        if model == ShortAnswerProblem:
            return ShortAnswerProblemSerializer
        elif model == DescriptiveProblem:
            return DescriptiveProblemSerializer
      
    def to_representation(self, instance):
        serializer = ProblemSerializer.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data

    @transaction.atomic
    def create(self, validated_data):
        serializerClass = ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
            validated_data['type']))
        serializer = serializerClass(validated_data)

        base_problem_data = validated_data.pop('base_problem')
        base_problem = BaseProblem.objects.create(**base_problem_data)
        base_problem.save()
        validated_data['base_problem'] = base_problem.pk
        
        return serializer.create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):    
        serializerClass = ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
            validated_data['type']))
        serializer = serializerClass(validated_data)

        validated_data['pk'] = instance.pk
        try:
            base_problem = instance.base_problem
            validated_data['base_problem']['pk'] = base_problem.pk
            base_problem.delete()
        except:
            pass
        instance.delete()
        instance = self.create(validated_data)
        return instance
        return serializer.update(instance, validated_data)

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class ProblemCategorySerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, required=False)
    mentors = BankAccountSerializer(many=True, required=False)
    viewers = BankAccountSerializer(many=True, required=False)
    
    class Meta:
        model = ProblemCategory
        fields = '__all__'

    def create(self, validated_data):
        if 'problems' in validated_data:
            validated_data.pop('problems')
        if 'mentors' in validated_data:
            validated_data.pop('mentors')
        if 'viewers' in validated_data:
            validated_data.pop('viewers')

        instance = ProblemCategory.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('problems')
        validated_data.pop('mentors')
        validated_data.pop('viewers')
        validated_data.pop('fsm')
        validated_data['pk'] = instance.pk
        instance.delete()
        instance = self.create(validated_data)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



class GuidanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guidance
        fields = '__all__'


