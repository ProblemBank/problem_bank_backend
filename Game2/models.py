from django.db import models
from django.utils import timezone

from problembank.models import ProblemGroup, Problem
from Account.models import User
from constants import MAX_CARROUSEL_TURNS, OPEN_BOX_COST


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
        Room, on_delete=models.PROTECT, related_name='current_room', null=True, blank=True)
    users = models.ManyToManyField(
        User, related_name='team', verbose_name='اعضا')
    chat_room = models.URLField(
        max_length=100, verbose_name='اتاق قرار', null=True, blank=True)
    carrousel_turn = models.IntegerField(
        default=MAX_CARROUSEL_TURNS, verbose_name='تعداد دفعات باقی مانده چرخاندن گردونه')
    first_entrance = models.FloatField(null=True, blank=True)
    group_problems = models.ManyToManyField(ProblemGroup, related_name='team')

    def __str__(self):
        return f'{self.name}'


class Box(models.Model):
    number = models.IntegerField(default=0, verbose_name='شماره')
    open_cost = models.IntegerField(
        default=OPEN_BOX_COST, verbose_name='هزینه باز کردن جعبه')
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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification', null=True, blank=True)
    has_seen = models.BooleanField(default=False)
    time = models.TimeField(default=timezone.now)

    def __str__(self):
        return f'title={self.title}\ntext = {self.body}\nteam={self.user}'


class GameInfo(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    floating_mode = models.BooleanField(default=True)
    problem_cost = models.IntegerField(default=100)
    easy_problem_reward = models.IntegerField(default=300)
    medium_problem_reward = models.IntegerField(default=400)
    hard_problem_reward = models.IntegerField(default=500)
    so_hard_problem_reward = models.IntegerField(default=600)
    max_room_number = models.IntegerField(default=5)
    last_room_cost = models.IntegerField(default=900)
    max_not_submitted_problems = models.IntegerField(default=2)
    last_room_name = models.CharField(max_length=128, default='')
    carrousel_win_ratio_reward = models.FloatField(default=1.5)
    carrousel_lose_ratio_reward = models.FloatField(default=0.5)
    max_time_to_play = models.FloatField(default=4*60*60)

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
