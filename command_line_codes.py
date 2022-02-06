from django.db.models import fields
from rest_framework import serializers

from Game.models import *
from problembank.models import *

from Account.serializers import CreateUserSerializer
from problembank.serializers import *

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
    



class UserRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name']

class PlayerRewardSerializer(serializers.ModelSerializer):
    users = UserRewardSerializer(many=True)
    class Meta:
        model = Player
        fields = ['users', 'name', 'coin', 'blue_toot', 'red_toot', 'black_toot',
                  'fake_checkable_objects', 'not_fake_checkable_objects']

import csv
def convert_all():
    players = Player.objects.all()
    datas = []
    for player in players:
        data = PlayerRewardSerializer(player).data
        try:
            data['user1'] = data['users'][0]['user_name']
        except:
            pass
        try:
            data['user2'] = data['users'][1]['user_name']
        except:
            pass
        try:
            data['user3'] = data['users'][2]['user_name']
        except:
            pass
        data.pop('users')
        datas.append(data)
    file = open('data_file.csv', 'w')
    with file:
        header = ['user1', 'user2', 'user3', 'name', 'coin', 'blue_toot', 'red_toot', 'black_toot',
                  'fake_checkable_objects', 'not_fake_checkable_objects']
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        for i in range(0, len(datas)):
            writer.writerow(datas[i])




global_problem_json_example ='''[{"title": "جایگشت آینه ای", "topics": ["ترکیبیات"],
 "subtopics": [{"topic": "ترکیبیات", "title": "ناوردایی"}], "source": "غیره",
  "difficulty": "Hard", "grade": "HighSchoolFirstHalf", "is_checked": false,
   "problem_type": "DescriptiveProblem", "author": {"first_name": "اضافه کننده",
    "last_name": "اضافه کننده زاده", "email": "moeini.erfan@yahoo.com", "phone_number": "09"},
    "text": "<p><span class=\\" author-d-1gg9uz65z1iz85zgdz68zmqkz84zo2qoxwz73zz70zz73zz78zydafz65zz84z5vm3wz72zz89zz80z0ogz88zdv3er1fz71z\\">از جایگشت </span><span class=\\" author-d-1gg9uz65z1iz85zgdz68zmqkz84zo2qoxwz73zz70zz73zz78zydafz65zz84z5vm3wz72zz89zz80z0ogz88zdv3er1fz71z\\"><span class=\\"inline-latex\\" data-inline-magic=\\"latex\\" data-current-latex-value=\\"a_1,a_2,\\\\cdots , a_n\\"><span class=\\"tiny-math\\" data-latex=\\"a_1,a_2,\\\\cdots , a_n\\"></span></span></span><span class=\\" author-d-1gg9uz65z1iz85zgdz68zmqkz84zo2qoxwz73zz70zz73zz78zydafz65zz84z5vm3wz72zz89zz80z0ogz88zdv3er1fz71z\\">باشد؟</span></p>", "publish_date": "2021-01-31T14:52:35.897617+03:30",
    "last_change_date": null, "is_private": false, "upvote_count": 0}]'''

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

def create_or_get_source_pk(title):
    if title is None:
        return None
    try:
        return Source.objects.filter(title=title)[0].pk
    except:
        return Source.objects.create(title=title).pk

class DescriptiveProblemSerializerForConvert(serializers.ModelSerializer):
    answer = DescriptiveAnswerSerializer(required=False)
    class Meta:
        model = DescriptiveProblem
        fields = '__all__'
       
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
        instance.is_checked = False
        instance.save()
    
        return instance

class ShortAnswerProblemSerializerForConvert(serializers.ModelSerializer):
    answer = ShortAnswerSerializer(required=False)
    class Meta:
        model = ShortAnswerProblem
        fields = '__all__'
       
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
        instance.is_checked = False
        instance.save()
    
        return instance

def craete_or_get_problem_group(event, problem_group):
    try:
        return ProblemGroup.objects.get(title=problem_group, event=event)
    except:
        pass
    return ProblemGroup.objects.create(title=problem_group, event=event)

def create_problem_with_global_problem_json(problem_json_object):
    problem_data = problem_json_object.copy()
    problem_data['topics'] = [create_or_get_topic(topic).pk for topic in problem_data['topics']]
    problem_data['subtopics'] = [create_or_get_subtopic(subtopic['topic'], subtopic['title']).pk for subtopic in problem_data['subtopics']]
    problem_data['source'] = create_or_get_source_pk(problem_data['source'])

    problem_data['author'] = create_or_get_account(problem_data['author'])
    problem_data['answer'] = json.loads('{"text":"بدون پاسخ"}')

    problem_data['is_private'] = True
            
    event = None
    problem_group = None
    try:
        for pg in problem_data['problem_groups']:
            event = pg['event']
            problem_group = pg['title']
    except:
        print("bad")
        pass
    if event is None:
        event = 'مسابقه‌ی توتنخ‌عامو'
        problem_group = 'همه'
    
    if problem_data['problem_type'] == Problem.Type.ShortAnswerProblem:
        problemSerializer = ShortAnswerProblemSerializerForConvert(data=problem_data)
    else:
        problemSerializer = DescriptiveProblemSerializerForConvert(data=problem_data)
    problemSerializer.is_valid(raise_exception=True)
    data = problemSerializer.validated_data
    instance = problemSerializer.create(data)

    if event is not None:
        event = Event.objects.get(title=event)
        if problem_group is not None:
            problem_group = craete_or_get_problem_group(event, problem_group)
            problem_group.problems.add(instance)
            problem_group.save()
        else:
            print("error!!", event.title)
    return instance

def create_many_problem_with_global_problem_json(problems_json):
    problems_json_object = json.loads(problems_json)
    for problem_json_object in problems_json_object:
        create_problem_with_global_problem_json(problem_json_object)
    
f = open("out.json", "r")
create_many_problem_with_global_problem_json(f.read())
f.close()
# datas = []
# for registerrec in RegistrationReceipt.objects.all():
#     if registerrec.is_participating:
#         data = {}
#         data['password'] = registerrec.user.password
#         try:
#             data['team'] = registerrec.team.id
#         except:
#             data['team'] = None
#         data['first_name'] = registerrec.user.first_name
#         data['last_name'] = registerrec.user.last_name
#         data['ph
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
    # one_number'] = registerrec.user.username
#         datas.append(data)

# with file:
#     header = ['password', 'team', 'first_name', 'last_name', 'phone_number']
#     writer = csv.DictWriter(file, fieldnames = header)
#     writer.writeheader()
#     for i in range(0, len(datas)):
#     writer.writerow(datas[i])


# from problembank.models import *
# pgs = ProblemGroup.objects.filter(event=3)
# q = Problem.objects.filter(pk=-1)
# for pg in pgs:
#     q = q | pg.problems.all()
# for p in q:
#     p.grade = Problem.Grade.HighSchoolFirstHalf
#     p.save()