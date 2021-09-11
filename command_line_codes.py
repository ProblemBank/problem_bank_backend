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




global_problem_json_example =''' {
    "base_problem": {
        "title": "پترسن اول",
        "topics": ["ترکیبیات"],from problembank.serializers import BankAccountSerializer, create_or_get_topic

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

def create_or_get_source_pk(title):
    if title is None:
        return None
    try:
        return Source.objects.filter(title=title)[0].pk
    except:
        return Source.objects.create(title=title).pk

def create_problem_with_global_problem_json(problem_json_object):
    base_problem_data = problem_json_object['base_problem']
    base_problem_data['topics'] = [create_or_get_topic(topic).pk for topic in base_problem_data['topics']]
    base_problem_data['subtopics'] = [create_or_get_subtopic(subtopic['topic'], subtopic['title']).pk for subtopic in base_problem_data['subtopics']]
    base_problem_data['source'] = create_or_get_source_pk(base_problem_data['source'])

    # baseProblemSerializer = BaseProblemSerializer(data=base_problem_data)
    # baseProblemSerializer.is_valid(raise_exception=True)

    # problem_json_object['base_problem'] = baseProblemSerializer.create(baseProblemSerializer.validated_data).pk
    problem_json_object['author'] = create_or_get_account(problem_json_object['author'])
    problem_json_object['answer'] = json.loads('{"text":"بدون پاسخ"}')
    descriptiveProblemSerializer = DescriptiveProblemSerializer(data=problem_json_object)
    descriptiveProblemSerializer.is_valid(raise_exception=True)
    return descriptiveProblemSerializer.create(descriptiveProblemSerializer.validated_data)

def create_many_problem_with_global_problem_json(problems_json):
    problems_json_object = json.loads(problems_json)
    for problem_json_object in problems_json_object:
        create_problem_with_global_problem_json(problem_json_object)
    
'[{"base_problem": {"title": "erty", "topics": ["ترکیبیات"], "subtopics": [{"topic": "ترکیبیات", "title": "لانه کبوتری"}, {"topic": "ترکیبیات", "title": "استقرا"}], "source": null, "difficulty": "VeryEasy", "suitable_for_over": 1, "suitable_for_under": 12, "is_checked": false}, "problem_type": "DescriptiveProblem", "title": "erty", "author": {"first_name": "sdf", "last_name": "None", "email": "wef", "phone_number": "09"}, "text": "derfghjn", "publish_date": "2021-09-06T17:49:54.043791+04:30", "last_change_date": null, "is_private": false, "upvoteCount": 0}, {"base_problem": {"title": "lkjpo;lasfdasdf", "topics": ["ترکیبیات"], "subtopics": [{"topic": "ترکیبیات", "title": "لانه کبوتری"}, {"topic": "ترکیبیات", "title": "استقرا"}], "source": "آنالیز ترکیبی", "difficulty": "Easy", "suitable_for_over": 1, "suitable_for_under": 12, "is_checked": false}, "problem_type": "DescriptiveProblem", "title": "lkjpo;lasfdasdf", "author": {"first_name": "sdf", "last_name": "None", "email": "wef", "phone_number": "09"}, "text": "slkdnf;sdf;llefwef", "publish_date": "2021-09-07T00:16:58.108720+04:30", "last_change_date": null, "is_private": false, "upvoteCount": 0}, {"base_problem": {"title": "mm", "topics": ["ترکیبیات", "هندسه"], "subtopics": [{"topic": "ترکیبیات", "title": "ناوردایی"}, {"topic": "هندسه", "title": "همساز"}], "source": "آنالیز ترکیبی", "difficulty": "Hard", "suitable_for_over": 5, "suitable_for_under": 7, "is_checked": false}, "problem_type": "DescriptiveProblem", "title": "mm", "author": {"first_name": "sdf", "last_name": "None", "email": "wef", "phone_number": "09"}, "text": "لاذتدنمپک", "publish_date": "2021-09-07T00:17:52.200124+04:30", "last_change_date": null, "is_private": false, "upvoteCount": 0}]'


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