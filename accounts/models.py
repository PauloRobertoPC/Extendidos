from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from django.urls import reverse, reverse_lazy

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, default="email@gmail.com")
    username = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    description = models.TextField(default="Descrição sobre você...")
    is_student = models.BooleanField(default=False)
    is_ong = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse_lazy('home')

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user.is_student = True
    registration = models.CharField(max_length=30, default='0')

class Ong(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user.is_ong = True
    cnpj = models.CharField(max_length=30, default='0')
