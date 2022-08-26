from django.db import models
from django.utils import timezone

from problembank.models import ProblemGroup, Problem
from Account.models import User
from constants import MAX_CARROUSEL_TURNS


class Room(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    entrance_cost = models.IntegerField(
        default=0, verbose_name='هزینه ورود به اتاق')
    problem_groups = models.ManyToManyField(
        ProblemGroup, verbose_name='گروه‌مسئله‌ها')

    def __str__(self):
        return f'{self.name}'


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    coin = models.IntegerField(default=700, verbose_name='پول')

    current_room = models.ForeignKey(
        Room, on_delete=models.PROTECT, related_name='current_room')
    leader = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='leader')
    users = models.ManyToManyField(
        User, related_name='users', verbose_name='اعضا')
    chat_room = models.URLField(
        max_length=100, verbose_name='اتاق قرار', null=True, blank=True)
    carrousel_turn = models.IntegerField(
        default=MAX_CARROUSEL_TURNS, verbose_name='تعداد دفعات باقی مانده چرخاندن گردونه')

    def __str__(self):
        return f'{self.name}'


class Box(models.Model):
    number = models.IntegerField(default=0, verbose_name='شماره')
    open_cost = models.IntegerField(
        default=0, verbose_name='هزینه باز کردن جعبه')
    reward = models.IntegerField(default=0, verbose_name='جایزه باز کردن جعبه')

    def __str__(self):
        return f'Box: cost={self.open_cost} reward={self.reward}'


class Carrousel(models.Model):
    invest_amount = models.IntegerField(default=0, blank=True, null=True)
    outcome_amount = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f'invest={self.invest_amount} outcome={self.outcome_amount}'


class Notification(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.CharField(max_length=200, blank=True, null=True)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='notification')
    has_seen = models.BooleanField(default=False)
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f'title={self.title}\ntext = {self.body}\nteam={self.team}'


class GameInfo(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'start={self.start_time} finish={self.finish_time}'


class TeamBox(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team_box')
    box = models.ForeignKey(
        Box, on_delete=models.CASCADE, related_name='team_box')


class TeamRoom(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team_room')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='team_room')
