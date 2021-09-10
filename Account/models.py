from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    class Grade(models.TextChoices):
        FIRST = 'FIRST'
        SECOND = 'SECOND'
        THIRD = 'THIRD'
        FORTH = 'FORTH'
        FIFTH = 'FIFTH'
        SIXTH = 'SIXTH'
        SEVENTH = 'SEVENTH'
        EIGHTH = 'EIGHTH'
        NINTH = 'NINTH'
        TENTH = 'TENTH'
        ELEVENTH = 'ELEVENTH'
        TWELFTH = 'TWELFTH'

    phone_number = models.CharField(max_length=15, blank=False, null=False)
    backup_phone_number = models.CharField(max_length=15, blank=False, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=Gender.choices)
    grade = models.CharField(max_length=10, null=True, blank=True, choices=Grade.choices)

    def user_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name} | {self.username}'
