from django.db import models

from Account.models import User


class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    finish_date = models.DateTimeField(verbose_name='تاریخ پایان')
    maximum_number_of_received_problem = \
        models.IntegerField(default=2,
                            verbose_name='حداکثر تعداد سوالاتی که بازیکن در یک لحظه می‌تواند داشته باشد')

    def __str__(self):
        return self.title


class Subject(models.Model):
    title = models.CharField(max_length=30, verbose_name='عنوان')
    game = models.ManyToManyField(Game, verbose_name='آزمون', blank=True)

    def __str__(self):
        return f'{self.title}'


# todo: make "BaseProblem" model
class Problem(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'EASY'
        MEDIUM = 'MEDIUM'
        HARD = 'HARD'

    class Type(models.TextChoices):
        SHORT_ANSWER = 'SHORT_ANSWER'
        DESCRIPTIVE = 'DESCRIPTIVE'

    title = models.CharField(max_length=100, verbose_name='عنوان')
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.DESCRIPTIVE, verbose_name='نوع')
    games = models.ManyToManyField(Game, verbose_name='بازی‌(ها)')
    subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, verbose_name='درجه سختی',
                                  default=Difficulty.MEDIUM)
    cost = models.IntegerField(default=0, verbose_name='هزینه‌ی دریافت')
    reward = models.IntegerField(default=0, verbose_name='پاداش حل‌کردن')
    text = models.TextField(verbose_name='متن')
    answer = models.TextField(null=True, blank=True, verbose_name='پاسخ (اختیاری)')
    relative_order = models.IntegerField(default=0, verbose_name='ترتیب نسبی')

    def __str__(self):
        return f'{self.title} ({"کوتاه پاسخ" if self.type == "SHORT_ANSWER" else "تشریحی"}، ' \
               f'{"آسان" if self.difficulty == "EASY" else ("متوسط" if self.difficulty == "MEDIUM" else "سخت")})'


# add game field
class MultipleProblem(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان', blank=True)
    problems = models.ManyToManyField(Problem, verbose_name='مسئله‌ها')
    maximum_hint_count = models.IntegerField(default=3, verbose_name='حداکثر تعداد راهنمایی')
    cost = models.IntegerField(default=0, verbose_name='هزینه‌ی دریافت')
    reward = models.IntegerField(default=0, verbose_name='پاداش حل‌کردن')


class Player(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='کاربر')
    game = models.ForeignKey(to=Game, on_delete=models.PROTECT, verbose_name='بازی')
    score = models.IntegerField(default=0, verbose_name='امتیاز')

    def __str__(self):
        return f'{self.user} | {self.game.title}'


# abstract
class PlayerProblem(models.Model):
    class Status(models.Choices):
        RECEIVED = 'RECEIVED'
        DELIVERED = 'DELIVERED'
        SCORED = 'SCORED'

    player = models.ForeignKey(Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RECEIVED, verbose_name='وضعیت')
    mark = models.IntegerField(default=-1, verbose_name='نمره')


class PlayerSingleProblem(PlayerProblem):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT, verbose_name='مسئله')
    text_answer = models.TextField(verbose_name='متن پاسخ')
    file_answer = models.FileField(upload_to='game-answers/', blank=True, null=True)


class PlayerMultipleProblem(PlayerProblem):
    multiple_problem = models.ForeignKey(MultipleProblem, on_delete=models.PROTECT, blank=True)
    step = models.IntegerField(default=0, verbose_name='تعداد سوالات حل‌شده تا اینجا')

    def __str__(self):
        return f'{self.player} | {self.multiple_problem.title}'


# todo: remove multiple_problem and replace player_multiple_problem
class Hint(models.Model):
    multiple_problem = models.ForeignKey(MultipleProblem, on_delete=models.PROTECT, verbose_name='مسئله چندتایی')
    player = models.ForeignKey(Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    question = models.TextField(verbose_name='ابهام')
    answer = models.TextField(verbose_name='پاسخ به ابهام', blank=True, null=True)
    is_answered = models.BooleanField(default=False, verbose_name='آیا رسیدگی شده؟')


class Transaction(models.Model):
    player = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    amount = models.IntegerField(verbose_name='مقدار')

    def __str__(self):
        return f'{self.title} | {self.player}'
