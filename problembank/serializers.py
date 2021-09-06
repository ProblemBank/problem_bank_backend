from django.db.models import base
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import sys
from .models import *
from django.db import transaction
import json



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
            validated_data['answer_type']))
        serializer = serializerClass(validated_data)
        return serializer.create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        serializerClass = AnswerSerializer.get_serializer(getattr(sys.modules[__name__],\
            validated_data['answer_type']))
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
        answer_data['answer_type'] = 'ShortAnswer'
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
    answer = DescriptiveAnswerSerializer(required=False)
    class Meta:
        model = DescriptiveProblem
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        answer_data = validated_data.pop('answer')
        instance = DescriptiveProblem.objects.create(**validated_data)
        answer_data['answer_type'] = 'DescriptiveAnswer'
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

class SimpleProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('base_problem',)


class ProblemSerializer(serializers.ModelSerializer):
    base_problem = BaseProblemSerializer()
    @classmethod
    def get_serializer(cls, model):
        print(model)
        if model == ShortAnswerProblem:
            return ShortAnswerProblemSerializer
        elif model == DescriptiveProblem:
            return DescriptiveProblemSerializer
        elif model == Problem:  
            return SimpleProblemSerializer
      
    @transaction.atomic
    def create(self, validated_data):
        serializerClass = ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
            validated_data['problem_type']))
        serializer = serializerClass(validated_data)

        base_problem_data = validated_data.pop('base_problem')
        base_problem = BaseProblem.objects.create(**base_problem_data)
        base_problem.save()
        validated_data['base_problem'] = base_problem.pk
        
        return serializer.create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):    
        serializerClass = ProblemSerializer.get_serializer(getattr(sys.modules[__name__],\
            validated_data['problem_type']))
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

    def to_representation(self, instance):
        print(instance, instance.__class__)
        serializer = ProblemSerializer.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data


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


class ProblemCategoryGetSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True)
    mentors = BankAccountSerializer(many=True)
    viewers = BankAccountSerializer(many=True)

    class Meta:
        model = ProblemCategory
        fields = '__all__'
   

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



class GuidanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guidance
        fields = '__all__'


global_problem_json_example =''' {
    "base_problem": {
        "title": "پترسن اول",
        "topics": ["ترکیبیات"],
        "subtopics": [
                {
                    "topic": "ترکیبیات", "title": "لانه کبوتری"
                },
                {
                    "topic": "ترکیبیات", "title": "استقرا"
                }
            ],
        "source": null,
        "difficulty": "VeryHard",
        "suitable_for_over": 10,
        "suitable_for_under": 12,
        "is_checked": false
        },
    "problem_type": "DescriptiveProblem",
    "title": "پترسن اول",
    "author": {
        "first_name": "erfan",
        "last_name": "moeini",
        "email": "erfan@google.com",
        "phone_number": "0912345"
        }, 
    "text": "ویژگی های زیر را در گراف پترسن بررسی کنید:\\r\\n\\r\\n![گراف پترسن](https://drive.google.com/open?id=1ZRkMeW100FgBJvzzaUhemVXebPamyOrZ)\\r\\n\\r\\n1. هر جفت راس که به هم متصل نیستند، دقیقا یک همسایه دارند.\\r\\n2. دور به طول هفت نداریم.\\r\\n3. دو دور به طول پنج، همه ی راس ها را پوشش میدهند.\\r\\n4. اندازه ی بزرگترین مجموعه مستقل در این گراف چهار است.", 
    "publish_date": "2021-05-25T20:08:17.081083+04:30",
    "last_change_date": null, 
    "is_private": false, 
    "upvoteCount": -6
}
'''
def create_or_get_account(account):
    try:
        return BankAccount.objects.filter(email=account['email'])[0].pk
    except:
        pass
    try:
        return BankAccount.objects.filter(phone_number=account['phone_number'])[0].pk
    except:
        pass
    try:
        return BankAccount.objects.filter(first_name=account['first_naem'], last_name=account['last_name'])[0].pk
    except:
        pass

    accountSerializer = BankAccountSerializer(data=account)
    accountSerializer.is_valid()
    return accountSerializer.create(accountSerializer.validated_data).pk

def create_or_get_topic(title):
    try:
        return Topic.objects.filter(title=title)[0]
    except:
        return Topic.objects.create(title=title)

def create_or_get_subtopic(topic_title, title):
    topic = create_or_get_topic(topic_title)
    try:
        return Subtopic.objects.filter(title=title, topic=topic)[0]
    except:
        return Subtopic.objects.create(title=title, topic=topic)

def create_problem_with_global_problem_json(problem_json_object):
    base_problem_data = problem_json_object['base_problem']
    base_problem_data['topics'] = [create_or_get_topic(topic).pk for topic in base_problem_data['topics']]
    base_problem_data['subtopics'] = [create_or_get_subtopic(subtopic['topic'], subtopic['title']).pk for subtopic in base_problem_data['subtopics']]
    
    baseProblemSerializer = BaseProblemSerializer(data=base_problem_data)
    baseProblemSerializer.is_valid(raise_exception=True)

    problem_json_object['base_problem'] = baseProblemSerializer.create(baseProblemSerializer.validated_data).pk
    problem_json_object['author'] = create_or_get_account(problem_json_object['author'])
    problem_json_object['answer'] = json.loads('{"text":"بدون پاسخ"}')
    descriptiveProblemSerializer = DescriptiveProblemSerializer(data=problem_json_object)
    descriptiveProblemSerializer.is_valid(raise_exception=True)
    return descriptiveProblemSerializer.create(descriptiveProblemSerializer.validated_data)

def create_many_problem_with_global_problem_json(problems_json):
    problems_json_object = json.loads(problems_json)
    for problem_json_object in problems_json_object:
        create_problem_with_global_problem_json(problem_json_object)
    