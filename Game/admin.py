import csv

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from Account.models import User
from Game.models import Player, Notification, Merchandise, CheckableObject, GameProblem, \
    Message, GroupMessage, FamousPerson, Exchange
from Account.serializers import CreateUserSerializer
admin.site.register(Merchandise)
admin.site.register(CheckableObject)
admin.site.register(GameProblem)
admin.site.register(Message)
admin.site.register(GroupMessage)
admin.site.register(Notification)
admin.site.register(FamousPerson)
admin.site.register(Exchange)


def import_from_csv(a, b, c):
    with open('students_info.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            user1 = User.objects.filter(username=row[2]).first()
            if user1 is None:
                data = {}
                data['password'] = make_password(row[2])
                data['username'] = row[2]
                data['first_name'] = row[3]
                data['last_name'] = row[4]
                data['phone_number'] = row[7]
                serializer = CreateUserSerializer(data=data)
                data = serializer.validated_data
                user = serializer.create(data)
                user.save()

                p, created = Player.objects.get_or_create(
                    score=row[0],
                    user=user)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    import_from_csv.short_description = 'بارگذاری دانش‌آموزان در سایت'
    actions = [import_from_csv]

    list_display = ('name', 'id')
