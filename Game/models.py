from django.db import models

from Account.models import User
from problembank.models import ProblemGroup


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
    famous_persons = models.ManyToManyField('FamousPerson', blank=True, verbose_name='اشخاص معروف')
    checkable_objects = models.ManyToManyField('CheckableObject', blank=True, verbose_name='اشیا')

    def __str__(self):
        return f'{self.name}'


class FamousPerson(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    is_fake = models.BooleanField(default=False, verbose_name='آیا تقلبی است؟')

    def __str__(self):
        return f'{self.name} | {self.is_fake}'


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


class Exchange(models.Model):
    seller = models.ForeignKey(to=Player, on_delete=models.PROTECT, verbose_name='فروشنده', related_name='seller')
    sold_merchandise = models.ForeignKey(to=Merchandise, on_delete=models.PROTECT, verbose_name='کالایی فروخته‌شده',
                                         related_name='sold_merchandise')
    buyer = models.ForeignKey(to=Player, on_delete=models.PROTECT, null=True, blank=True, verbose_name='خریدار',
                              related_name='buyer')
    bought_merchandise = models.ForeignKey(to=Merchandise, on_delete=models.PROTECT, verbose_name='کالایی خریداری‌شده',
                                           related_name='bought_merchandise')


class GameProblem(models.Model):
    reward_merchandise = models.ForeignKey(to=Merchandise, on_delete=models.PROTECT, verbose_name='کالا')
    problem_group = models.OneToOneField(ProblemGroup, null=True, on_delete=models.PROTECT,
                                         related_name='submit_answer', verbose_name='مسئله از بانک مسئله')
    famous_person = models.ForeignKey(to=FamousPerson, null=True, blank=True, on_delete=models.PROTECT,
                                      verbose_name='شخص معروف')

    def __str__(self) -> str:
        return f'{self.problem_group.title} ' + (f'{self.famous_person.name}' if self.famous_person else "")
