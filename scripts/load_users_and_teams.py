from Account.models import User
from Game2.models import Team
from Game2.serializers import CreateUserSerializer, TeamSerializer

import csv


def run():
    with open('../data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            user = User.objects.filter(last_name=row[3], first_name=row[2]).first()
            if user is None:
                data = {
                    'first_name': row[2],
                    'last_name': row[3],
                }
                user_serializer = CreateUserSerializer(data=data)
                data = user_serializer.validated_data
                user = user_serializer.create(validated_data=data)
                user.save()
                team = Team.objects.filter(users__in=[user]).first()
                if team is None:
                    team_data = {
                        'name': row[5],
                        'coin': 0,
                        'leader': user,
                        'users': [user],
                    }
                    team_serializer = TeamSerializer(data=team_data)
                    data = team_serializer.validated_data
                    team = team_serializer.create(validated_data=data)
                    team.save()
                else:
                    team.users.add(user)
                    team.save()

