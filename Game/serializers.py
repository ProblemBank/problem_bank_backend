from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from auction.models import Auction
from .models import *


# class HintSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Hint
#         fields = ['question', 'answer']


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
        model = Answer
        fields = '__all__'


# class MultipleProblemDetailedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CometProblem
#         fields = '__all__'


# class PlayerMultipleProblemDetailedSerializer(serializers.ModelSerializer):
#     multiple_problem = MultipleProblemDetailedSerializer()
#
#     class Meta:
#         model = CometProblemAnswer
#         fields = '__all__'


class ProblemInfoSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = Problem
        fields = ['id', 'title', 'cost', 'reward', 'subject', 'difficulty', ]


# class MultipleProblemInfoSerializer(serializers.ModelSerializer):
#     problems_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CometProblem
#         fields = ['id', 'cost', 'reward', 'title', 'problems_count']
#
#     def get_problems_count(self, obj):
#         return obj.problems.count()


class ProblemSerializer(serializers.ModelSerializer):
    problem = ProblemInfoSerializer()
    from_auction = SerializerMethodField('is_problem_bought_from_auction')
    auction_cost = SerializerMethodField('get_auction_cost')
    is_sold = SerializerMethodField('is_problem_sold_in_auction')

    def is_problem_bought_from_auction(self, answer):
        auction = Auction.objects.filter(buyer=answer.player, problem=answer.problem)
        if auction.exists():
            return True
        else:
            return False

    def is_problem_sold_in_auction(self, answer):
        auction = Auction.objects.filter(seller=answer.player, problem=answer.problem)
        if auction.exists():
            return True
        else:
            return False

    def get_auction_cost(self, answer):
        auction = Auction.objects.filter(buyer=answer.player, problem=answer.problem).first()
        return auction.price if auction else ''

    class Meta:
        model = Answer
        fields = ['id', 'status', 'mark', 'problem', 'from_auction', 'is_sold', 'auction_cost']


# class MultipleProblemSerializer(serializers.ModelSerializer):
#     multiple_problem = MultipleProblemInfoSerializer()
#
#     class Meta:
#         model = CometProblemAnswer
#         fields = ['id', 'status', 'mark', 'step', 'multiple_problem']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PlayerSerializer(serializers.ModelSerializer):
    users = UserSerializer()

    class Meta:
        model = Player
        fields = ['name', 'users', 'score']


class GetAnswerForCorrectionSerializer(serializers.ModelSerializer):
    problem = ProblemDetailedSerializer()
    from_auction = SerializerMethodField('is_problem_bought_from_auction')

    def is_problem_bought_from_auction(self, answer):
        auction = Auction.objects.filter(buyer=answer.player, problem=answer.problem)
        if auction.exists():
            return True
        else:
            return False

    class Meta:
        model = Answer
        fields = ['text_answer', 'file_answer', 'problem', 'id', 'from_auction']


# class HintAnsweringSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Hint
#         fields = ['question', 'id']
