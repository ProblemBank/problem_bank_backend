from django.db import models
from Game.models import Answer, Player, Problem
from django.core.validators import MaxValueValidator, MinValueValidator


class Auction(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان', null=True, blank=True)
    problem = models.ForeignKey(Problem, verbose_name='سوال برای فروش', on_delete=models.CASCADE, null=True)
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name='قیمت')
    seller = models.ForeignKey(Player, null=True, on_delete=models.PROTECT,
                               verbose_name='فروشنده', related_name='seller')
    buyer = models.ForeignKey(Player, on_delete=models.PROTECT, verbose_name='خریدار',
                              related_name='buyer', null=True, blank=True)
    done_deal = models.BooleanField(default=False, null=True, verbose_name='آیا خریداری شده؟')

    def __str__(self):
        return f'{self.seller.name} --> {self.buyer.name if self.buyer else "?"}'
