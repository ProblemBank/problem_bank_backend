
from django.db.models import base
from django.http.response import ResponseHeaders
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import sys
from problembank.models import *
from django.db import transaction
import json


class BankAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()

class BankSubtopicSerializer(serializers.Serializer):
    topic = serializers.CharField()
    title = serializers.CharField()

class BankCommentSerializer(serializers.Serializer):
    text = serializers.CharField()
    author = BankAccountSerializer()
    
class BankProblemSerializer(serializers.Serializer):
    title = serializers.CharField()
    topics = serializers.ListField(child=serializers.CharField())
    subtopics = serializers.ListField(child=BankSubtopicSerializer())
    source = serializers.CharField()
    difficulty = serializers.CharField()
    grade = serializers.CharField()
    is_checked = serializers.BooleanField()

    problem_type = serializers.CharField()
    
    author = BankAccountSerializer()

    text = serializers.CharField()
    publish_date =  serializers.DateTimeField()
    last_change_date =  serializers.DateTimeField()
    is_private = serializers.BooleanField()
    upvote_count = serializers.IntegerField()
    
    

def convert_question_to_global_problem(question):
    class Problem():
        pass
    problem = Problem()
    problem.title = question.title
    problem.topics = [tag.title for tag in question.topics.all()]
    problem.subtopics = []
    for subtag in question.subtopics.all():
        st = Problem()
        st.topic = subtag.topic.title
        st.title = subtag.title
        problem.subtopics.append(st)
    problem.source = question.source.title if question.source else None
    problem.difficulty = question.difficulty
    problem.grade = 'HighSchoolFirstHalf'
    problem.is_checked = False
    
    problem.problem_type = question.problem_type
    
    problem.author = Problem()
    problem.author.email = question.author.email
    problem.author.phone_number = question.author.phone_number
    problem.author.first_name = question.author.first_name
    problem.author.last_name = question.author.last_name
    
    problem.text = question.text
    problem.publish_date = question.publish_date
    problem.last_change_date = question.last_change_date
    problem.is_private = False
    problem.upvote_count = question.upvote_count
    
    # problem.answer = question.answer.text

    # problem.comments = []
    # for comment in question.comments.all():
    #     c = Problem()
    #     c.text = comment.text
    #     c.auth
from django.db.models import base
from django.http.response import ResponseHeaders
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
import sys
from problembank.models import *
from django.db import transaction
import json


class BankAccountSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()

class BankSubtopicSerializer(serializers.Serializer):
    topic = serializers.CharField()
    title = serializers.CharField()

class BankCommentSerializer(serializers.Serializer):
    text = serializers.CharField()
    author = BankAccountSerializer()

class BankProblemGroupSerializer(serializers.Serializer):
    event = serializers.CharField()
    title = serializers.CharField()

class BankProblemSerializer(serializers.Serializer):
    title = serializers.CharField()
    topics = serializers.ListField(child=serializers.CharField())
    subtopics = serializers.ListField(child=BankSubtopicSerializer())
    source = serializers.CharField()
    difficulty = serializers.CharField()
    grade = serializers.CharField()
    is_checked = serializers.BooleanField()

    problem_type = serializers.CharField()
    
    author = BankAccountSerializer()

    text = serializers.CharField()
    publish_date =  serializers.DateTimeField()
    last_change_date =  serializers.DateTimeField()
    is_private = serializers.BooleanField()
    upvote_count = serializers.IntegerField()
    
    problem_groups = serializers.ListField(child=BankProblemGroupSerializer())
    
    

def convert_question_to_global_problem(question):
    class Problem():
        pass
    problem = Problem()
    problem.title = question.title
    problem.topics = [tag.title for tag in question.topics.all()]
    problem.subtopics = []
    for subtag in question.subtopics.all():
        st = Problem()
        st.topic = subtag.topic.title
        st.title = subtag.title
        problem.subtopics.append(st)
    problem.source = question.source.title if question.source else None
    problem.difficulty = question.difficulty
    problem.grade = 'HighSchoolFirstHalf'
    problem.is_checked = False
    
    problem.problem_type = question.problem_type
    
    problem.author = Problem()
    problem.author.email = question.author.email
    problem.author.phone_number = question.author.phone_number
    problem.author.first_name = question.author.first_name
    problem.author.last_name = question.author.last_name
    
    problem.text = question.text
    problem.publish_date = question.publish_date
    problem.last_change_date = question.last_change_date
    problem.is_private = False
    problem.upvote_count = question.upvote_count
    
    problem_groups = ProblemGroup.objects.filter(problems__in=[question])
    problem.problem_groups = []
    for problem_group in problem_groups:
        pg = Problem()
        pg.title = problem_group.title
        pg.event = problem_group.event.title
        problem.problem_groups.append(pg)

    # problem.answer = question.answer.text

    # problem.comments = []
    # for comment in question.comments.all():
    #     c = Problem()
    #     c.text = comment.text
    #     c.author = Problem()
    #     c.author.email = comment.writer.email
    #     c.publish_date = cooment.publish_date()
    #     problem.comments.append(c)
    return problem
    
def convert_all_question_to_global_problem_json():
    problems = []
    for question in Problem.objects.all():
        problem = convert_question_to_global_problem(question)
        problems.append(problem)
    problems_json = json.dumps(BankProblemSerializer(problems, many=True).data, ensure_ascii=False)
    return problems_json
    #or = Problem()
    #     c.author.email = comment.writer.email
    #     c.publish_date = cooment.publish_date()
    #     problem.comments.append(c)
    return problem
    
def convert_all_question_to_global_problem_json():
    problems = []
    for question in Problem.objects.all():
        problem = convert_question_to_global_problem(question)
        problems.append(problem)
    problems_json = json.dumps(BankProblemSerializer(problems, many=True).data, ensure_ascii=False)
    return problems_json

from problembank.models import *
# from client import *
f = open("out.json", "w")
f.write(convert_all_question_to_global_problem_json())
f.close()
# docker cp summer_event_docker_bank_backend_1:\usr/src/app/out.json .