from django.db import models

from Account.models import User
from problembank.models import Problem


class Player(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    users = models.ManyToManyField(User, verbose_name='کاربر(ان)')

    coin = models.IntegerField(default=0, verbose_name='سکه')
    blue_toot = models.IntegerField(default=0, verbose_name='توت آبی')
    red_toot = models.IntegerField(default=0, verbose_name='توت قرمز')
    black_toot = models.IntegerField(default=0, verbose_name='توت سیاه')

    has_find_TABOOT = models.BooleanField(default=False, verbose_name='آیا تابوت توتنخ‌عامو رو پیدا کرده‌اند؟')
    has_answered_first_problem = models.BooleanField(default=False, verbose_name='آیا سوال اولیه رو پاسخ داده است؟')
    number_of_free_check = models.IntegerField(default=0,
                                               verbose_name='تعداد بارهایی که بازیکن می‌تواند به صورت رایگان عمل چک‌کردن را انجام دهد')
    has_found_famous_person1 = models.BooleanField(default=False,
                                                   verbose_name='آیا نفر اول تو تالار مشاهیر رو یافته‌اند؟')
    has_found_famous_person2 = models.BooleanField(default=False,
                                                   verbose_name='آیا نفر دوم تو تالار مشاهیر رو یافته‌اند؟')

    def __str__(self):
        return f'{self.name}'


class Merchandise(models.Model):
    coin = models.IntegerField(default=0, verbose_name='سکه')
    blue_toot = models.IntegerField(default=0, verbose_name='توت آبی')
    red_toot = models.IntegerField(default=0, verbose_name='توت قرمز')
    black_toot = models.IntegerField(default=0, verbose_name='توت سیاه')

    def __str__(self):
        return f'سکه: {self.coin} - توت آبی: {self.blue_toot} - توت قرمز: {self.red_toot} - توت سیاه: {self.black_toot}'


class CheckableObject(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    merchandise = models.ForeignKey(to=Merchandise, on_delete=models.PROTECT, verbose_name='کالا')
    image = models.ImageField(upload_to='TootenkhAmoo/checkable_objects/', blank=True, null=True, verbose_name='تصویر')


class PlayerCheckableObject(models.Model):
    checkable_object = models.ForeignKey(to=CheckableObject, on_delete=models.PROTECT, verbose_name='شی')
    player = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    is_checked = models.BooleanField(default=False, verbose_name='آیا بازیکن، شی را بررسی کرده؟')


class Message(models.Model):
    text = models.CharField(max_length=50, verbose_name='پیام')
    image = models.ImageField(upload_to='TootenkhAmoo/messages/', blank=True, null=True, verbose_name='تصویر')
    order = models.IntegerField(default=0, verbose_name='ترتیب نسبی')


class GroupMessage(models.Model):
    messages = models.ManyToManyField(to=Message, verbose_name='پیام‌ها')


class Notification(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    body = models.TextField(verbose_name='متن')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='کاربر')
    time = models.TimeField(verbose_name='زمان')
    has_seen = models.BooleanField(default=False, verbose_name='آیا مشاهده کرده؟')


class GameProblem(models.Model):
    merchandise = models.ForeignKey(to=Merchandise, on_delete=models.PROTECT, verbose_name='کالا')
    problem = models.ForeignKey(to=Problem, on_delete=models.PROTECT, verbose_name='مسئله از بانک مسئله')
