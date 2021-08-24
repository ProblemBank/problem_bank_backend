from django.db import models
from Game.models import ProblemAnswer, Player, Problem
from django.core.validators import MaxValueValidator, MinValueValidator


class Auction(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    problem_for_sell = models.ForeignKey(Problem, verbose_name='سوال برای فروش', on_delete=models.CASCADE, null=True)
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name='قیمت')
    player = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    done_deal = models.BooleanField(default=False, null=True, verbose_name='خریداری شده')

    def __str__(self):
        return self.title
