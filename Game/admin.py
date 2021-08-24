import csv

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from Account.models import User
from Game.models import Game, Player, Transaction, Subject, Hint, CometProblemAnswer, \
    ProblemAnswer, Problem, CometProblem

admin.site.register(CometProblem)
admin.site.register(CometProblemAnswer)
admin.site.register(Game)
admin.site.register(Subject)


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


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass
    # list_display = ('title', 'type', 'difficulty', 'cost', 'reward', 'answer')


def girls_scores(a, b, c):
    all_transaction = Transaction.objects.all()
    for transaction in all_transaction:
        if transaction.title == 'ماین' or transaction.title == 'بانک' or transaction.title == 'بازی':
            transaction.player.score += transaction.amount
            transaction.player.save()


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'player', 'amount')
    actions = [girls_scores]
    girls_scores.short_description = 'هندل‌کردن امتیاز دخترها'


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('answer', 'is_answered')


@admin.register(ProblemAnswer)
class PlayerSingleProblemAdmin(admin.ModelAdmin):
    list_display = ('player', 'problem', 'status', 'mark')
