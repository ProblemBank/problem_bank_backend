import csv

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from Account.models import User
from Game.models import Player, Notification, Merchandise, CheckableObject, GameProblem, PlayerCheckableObject, \
    Message, GroupMessage

admin.site.register(Merchandise)
admin.site.register(CheckableObject)
admin.site.register(GameProblem)
admin.site.register(PlayerCheckableObject)
admin.site.register(Message)
admin.site.register(GroupMessage)
admin.site.register(Notification)


def import_from_csv(a, b, c):
    with open('students_info.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            user1 = User.objects.filter(username=row[2]).first()
            if user1 is None:
                user = User(
                    password=make_password(row[2]),
                    username=row[2],
                    first_name=row[3],
                    last_name=row[4],
                    phone_number=row[7],
                    backup_phone_number=row[8]
                )
                user.save()
                p, created = Player.objects.get_or_create(
                    score=row[0],
                    user=user)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    import_from_csv.short_description = 'بارگذاری دانش‌آموزان در سایت'
    actions = [import_from_csv]

    list_display = ('name', 'id')
