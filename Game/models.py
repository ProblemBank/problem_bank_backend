from django.db import models

from Account.models import User


class Player(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام بازیکن')
    users = models.ManyToManyField(User, verbose_name='کاربر(ان)')

    money = models.IntegerField(default=0, verbose_name='پول')
    blue_toot = models.IntegerField(default=0, verbose_name='توت آبی')
    red_toot = models.IntegerField(default=0, verbose_name='توت قرمز')
    black_toot = models.IntegerField(default=0, verbose_name='توت سیاه')

    has_answered_first_problem = models.BooleanField(default=False, verbose_name='آیا سوال اولیه رو پاسخ داده است؟')

    def __str__(self):
        return f'{self.name}'


class CheckableObject(models.Model):
    blue_toot = models.IntegerField(default=0, verbose_name='توت آبی')
    red_toot = models.IntegerField(default=0, verbose_name='توت قرمز')
    black_toot = models.IntegerField(default=0, verbose_name='توت سیاه')


class PlayerCheckableObject(models.Model):
    checkable_object = models.ForeignKey(to=CheckableObject, on_delete=models.PROTECT, verbose_name='شی')
    player = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='بازیکن')
    is_checked = models.BooleanField(default=False, verbose_name='آیا بازیکن، شی را بررسی کرده؟')


class Message(models.Model):
    text = models.CharField(max_length=50, verbose_name='پیام')
    image = models.ImageField(models.ImageField(upload_to='game/', blank=True, null=True))
    order = models.IntegerField(default=0, verbose_name='ترتیب نسبی')


class GroupMessage(models.Model):
    messages = models.ManyToManyField(to=Message)
