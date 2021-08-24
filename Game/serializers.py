from rest_framework import serializers
from .models import *


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ['question', 'answer']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title']


class ProblemDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ['answer', 'games']


class PlayerSingleProblemDetailedSerializer(serializers.ModelSerializer):
    problem = ProblemDetailedSerializer()

    class Meta:
        model = ProblemAnswer
        fields = '__all__'


class MultipleProblemDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CometProblem
        fields = '__all__'


class PlayerMultipleProblemDetailedSerializer(serializers.ModelSerializer):
    multiple_problem = MultipleProblemDetailedSerializer()

    class Meta:
        model = CometProblemAnswer
        fields = '__all__'


class ProblemInfoSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Problem
        fields = ['id', 'title', 'cost', 'reward', 'subject', 'difficulty', ]


class MultipleProblemInfoSerializer(serializers.ModelSerializer):
    problems_count = serializers.SerializerMethodField()

    class Meta:
        model = CometProblem
        fields = ['id', 'cost', 'reward', 'title', 'problems_count']

    def get_problems_count(self, obj):
        return obj.problems.count()


class SingleProblemSerializer(serializers.ModelSerializer):
    problem = ProblemInfoSerializer()

    class Meta:
        model = ProblemAnswer
        fields = ['id', 'status', 'mark', 'problem']


class MultipleProblemSerializer(serializers.ModelSerializer):
    multiple_problem = MultipleProblemInfoSerializer()

    class Meta:
        model = CometProblemAnswer
        fields = ['id', 'status', 'mark', 'step', 'multiple_problem']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PlayerSerializer(serializers.ModelSerializer):
    users = UserSerializer()

    class Meta:
        model = Player
        fields = ['name', 'users', 'score']


class PlayerSingleProblemCorrectionSerializer(serializers.ModelSerializer):
    problem = ProblemDetailedSerializer()

    class Meta:
        model = ProblemAnswer
        fields = ['text_answer', 'problem', 'id']


class HintAnsweringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ['question', 'id']
