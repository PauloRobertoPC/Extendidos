from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.urls import reverse_lazy

from .managers import CustomUserManager
from .utils import universities

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    description = models.TextField(default="")
    is_student = models.BooleanField(default=False)
    is_ong = models.BooleanField(default=False)
    cover = models.ImageField(upload_to="covers/", default='covers/default_cover.png')
    perfil = models.ImageField(upload_to="perfils/", default='perfils/default_perfil.png')
    sum_avaliation = models.IntegerField(default=0)
    total_avaliation = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def mean_avaliation(self):
        return round(self.sum_avaliation/max(self.total_avaliation, 1), 2)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('home')

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user.is_student = True
    university = models.CharField(max_length=100, choices=universities, default="Universidade Federal do Ceará")
    registration = models.CharField(max_length=30, default='0')

    def __str__(self):
        return self.user.username


class Ong(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user.is_ong = True
    cnpj = models.CharField(max_length=30, default='0')

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rated_user")
    comment = models.CharField(max_length=255)
    stars = models.IntegerField(default=0,
                                validators=[
                                    MinValueValidator(0),
                                    MaxValueValidator(5)
                                ]
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluator_user")

    def __str__(self):
        return self.comment
