from Account.models import User
from Game2.models import Team
from Game2.utils import create_team_room
from Game2.serializers import CreateUserSerializer, TeamSerializer
from problembank.models import BankAccount

import csv
from django.contrib.auth.hashers import make_password


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
                    'password': make_password(row[3]),
                    'last_name': row[4],
                    'gender': row[5].upper(),
                    'grade': row[7],
                }
                user_serializer = CreateUserSerializer(data=data)
                user_serializer.is_valid()
                user = user_serializer.create(validated_data=data)
                user.save()
            else:
                bank_account_data = {
                    'first_name': row[2],
                    'last_name': row[4],
                }
                password = make_password(row[3])
                user.password = password
                user.save()

            bank_account = BankAccount.objects.filter(
                **bank_account_data).first()
            if bank_account is None:
                bank_account = BankAccount.objects.create(
                    bank_account_data)
                bank_account.user = user
                bank_account.save()
            else:
                bank_account.user = user
                bank_account.save()

            team = Team.objects.filter(name=row[6]).first()
            if team is None:
                team = Team.objects.create(
                    name=row[6],
                    chat_room=row[8]
                )
                team.users.add(user)
                team.save()
            else:
                create_team_room(team)
                team.users.add(user)
                team.save()
