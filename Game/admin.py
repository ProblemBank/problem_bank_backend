import csv

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from Account.models import User
from Game.models import Game, Player, Subject, \
    Answer, Problem

admin.site.register(Game)


# with open(path) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         _, created = Teacher.objects.get_or_create(
#             first_name=row[0],
#             last_name=row[1],
#             middle_name=row[2],
#         )
#         # creates a tuple of the new object or
#         # current object and a boolean of if it was created


def import_from_csv(a, b, c):
    with open('students_info.csv') as f:
        reader = csv.reader(f)
        boys_game = Game.objects.get(title='پسرانه')
        girls_game = Game.objects.get(title='دخترانه')
        for row in reader:
            if row[5] == 'MAN':
                game = boys_game
            else:
                game = girls_game

            initial_user = User.objects.filter(username=row[2]).first()
            if initial_user is None:
                user = User(
                    password=make_password(row[2]),
                    username=row[2],
                    first_name=row[3],
                    last_name=row[4],
                    phone_number=row[7],
                    backup_phone_number=row[8]
                )
                user.save()
                Player.objects.get_or_create(
                    score=row[0],
                    user=user,
                    game=game)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    import_from_csv.short_description = 'بارگذاری دانش‌آموزان در سایت'
    actions = [import_from_csv]

    list_display = ('game', 'score', 'id')


# @admin.register(Transaction)
# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'player', 'amount')
#     actions = [girls_scores]
#     girls_scores.short_description = 'هندل‌کردن امتیاز دخترها'


# @admin.register(Hint)
# class HintAdmin(admin.ModelAdmin):
#     list_display = ('answer', 'is_answered')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('player', 'problem', 'status', 'mark')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']
  
# Edited part by atid:
@admin.register(Problem)
class BaseProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'subject', 'difficulty', 'cost', 'reward', 'answer']
    list_filter = ('subject',)

