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

    description = models.TextField()
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
    university = models.CharField(max_length=100, choices=universities, default="Universidade Federal do Ceará")
    registration = models.CharField(max_length=30, default='0')

class Ong(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user.is_ong = True
    cnpj = models.CharField(max_length=30, default='0')
    def __str__(self):
    	return self.user.email

