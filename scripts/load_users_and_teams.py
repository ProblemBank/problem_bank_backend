from Account.models import User
from Game2.models import Team
from Game2.serializers import CreateUserSerializer, TeamSerializer

import csv


def run():
    with open('data.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            user = User.objects.filter(username=row[0]).first()
            if user is None:
                data = {
                    'username': row[0],
                    'phone_number': row[1],
                    'first_name': row[2],
                    'password': row[3],
                    'last_name': row[4],
                    'gender': row[5].upper(),
                    'grade': row[7],
                }
                user_serializer = CreateUserSerializer(data=data)
                user_serializer.is_valid()
                user = user_serializer.create(validated_data=data)
                user.save()
                team = Team.objects.filter(name=row[6]).first()
                if team is None:
                    team_data = {
                        'name': row[6],
                        'chat_room': row[8]
                    }
                    team_serializer = TeamSerializer(data=team_data)
                    team_serializer.is_valid()
                    data = team_serializer.validated_data
                    team = team_serializer.create(validated_data=data)
                    team.users.add(user)
                    team.save()
                else:
                    team.users.add(user)
                    team.save()

