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
    games = models.ManyToManyField(Game, verbose_name='آزمون(ها)', blank=True)

    def __str__(self):
        return f'{self.title}'


class BaseProblem(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'EASY'
        MEDIUM = 'MEDIUM'
        HARD = 'HARD'

    class Type(models.TextChoices):
        SHORT_ANSWER = 'SHORT_ANSWER'
        DESCRIPTIVE = 'DESCRIPTIVE'
        COMET = 'COMET'
        GROUP = 'GROUP'

    title = models.CharField(max_length=100, verbose_name='عنوان')
    games = models.ManyToManyField(Game, verbose_name='بازی‌(ها)')

    type = models.CharField(max_length=20, choices=Type.choices, default=Type.DESCRIPTIVE, verbose_name='نوع')
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, verbose_name='سختی',
                                  default=Difficulty.MEDIUM)
    subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, blank=True, null=True, verbose_name='موضوع')

    cost = models.IntegerField(default=0, verbose_name='هزینه‌ی دریافت')
    reward = models.IntegerField(default=0, verbose_name='پاداش حل‌کردن')

    class Meta:
        abstract = True


class Problem(BaseProblem):
    text = models.TextField(verbose_name='متن')
    answer = models.TextField(null=True, blank=True, verbose_name='پاسخ (اختیاری)')

    def __str__(self):
        return f'{self.title} ({"کوتاه پاسخ" if self.type == "SHORT_ANSWER" else "تشریحی"}، ' \
               f'{"آسان" if self.difficulty == "EASY" else ("متوسط" if self.difficulty == "MEDIUM" else "سخت")})'


# class CometProblem(BaseProblem):
#     problems = models.ManyToManyField(Problem, verbose_name='مسئله(ها)')


class Player(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام بازیکن')
    users = models.ManyToManyField(User, verbose_name='کاربر(ان)')
    game = models.ForeignKey(to=Game, on_delete=models.PROTECT, verbose_name='بازی')
    score = models.IntegerField(default=0, verbose_name='امتیاز')

    def __str__(self):
        return f'{self.name}'


class BaseAnswer(models.Model):
    class Status(models.Choices):
        RECEIVED = 'RECEIVED'
        DELIVERED = 'DELIVERED'
        SCORED = 'SCORED'

    player = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.RECEIVED, verbose_name='وضعیت')
    mark = models.IntegerField(default=-1, verbose_name='نمره')


class Answer(BaseAnswer):
    problem = models.ForeignKey(Problem, on_delete=models.PROTECT, verbose_name='مسئله', related_name='problem')
    text_answer = models.TextField(verbose_name='پاسخ متنی')
    file_answer = models.FileField(upload_to='game-answers/', blank=True, null=True, verbose_name='فایل پاسخ')


# class CometProblemAnswer(BaseAnswer):
#     multiple_problem = models.ForeignKey(CometProblem, on_delete=models.PROTECT, blank=True)
#     step = models.IntegerField(default=0, verbose_name='تعداد سوالات حل‌شده تا اینجا')
#
#     def __str__(self):
#         return f'{self.player} | {self.multiple_problem.title}'


# class Hint(models.Model):
#     baseAnswer = models.ForeignKey(to=BaseAnswer, on_delete=models.PROTECT, verbose_name='پاسخ')
#     question = models.TextField(verbose_name='متن راهنمایی')
#     answer = models.TextField(verbose_name='پاسخ به راهنمایی', blank=True, null=True)
#     is_answered = models.BooleanField(default=False, verbose_name='آیا رسیدگی شده؟')


# class Transaction(models.Model):
#     player = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='بازیکن')
#     title = models.CharField(max_length=100, verbose_name='عنوان')
#     amount = models.IntegerField(verbose_name='مقدار')
#
#     def __str__(self):
#         return f'{self.title} | {self.player}'
