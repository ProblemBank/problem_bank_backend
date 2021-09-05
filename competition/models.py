from django.db import models
from Account.models import User
from model_utils.managers import InheritanceManager
from django.utils import timezone
from problembank import Problem, ShortAnswer, ShortAnswerSubmit



class GamingShortAnswerProblem(Problem):
    answer = models.OneToOneField(ShortAnswer, null=True, on_delete=models.SET_NULL, unique=True,
                                   related_name='problem', verbose_name='پاسخ صحیح')
    cost = models.IntegerField(default=0, verbose_name='هزینه‌ی دریافت') 
    reward = models.IntegerField(default=0, verbose_name='پاداش حل‌کردن')

class Game(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    finish_date = models.DateTimeField(verbose_name='تاریخ پایان')
    maximum_number_of_received_problem = \
        models.IntegerField(default=2,
                            verbose_name='حداکثر تعداد سوالاتی که بازیکن در یک لحظه می‌تواند داشته باشد')

    maximum_number_of_received_problem_per_subject = \
        models.IntegerField(default=6,
                            verbose_name='حداکثر تعداد سوالاتی که یک بازیکن در کل مسابقه از یک مبحث می‌تواند داشته باشد')

    def __str__(self):
        return self.title

class Player(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام بازیکن')
    users = models.ManyToManyField(User, verbose_name='کاربر(ان)')
    game = models.ForeignKey(to=Game, on_delete=models.PROTECT, verbose_name='بازی')
    score = models.IntegerField(default=0, verbose_name='امتیاز')

    def __str__(self):
        return f'{self.name}'
