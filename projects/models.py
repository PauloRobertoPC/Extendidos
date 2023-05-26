from django.db import models
from accounts.models import Ong,Student,CustomUser
from .utils import states
from django.urls import reverse_lazy

class Project(models.Model):
    ong = models.ForeignKey(Ong,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)    
    description = models.TextField()
    location = models.CharField(max_length=100, choices=states, default="Ceará")

    def get_absolute_url(self):
        return reverse_lazy('home')

    def __str__(self):
        return self.title

class Job(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    student = models.ManyToManyField(Student,null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, choices=states, default="Ceará")
    available_vacancies = models.IntegerField()
    job_begin =  models.DateField()
    job_end = models.DateField()

    def get_absolute_url(self):
        return reverse_lazy('home')

    def __str__(self):
        return self.title

class Notification(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    message = models.CharField(max_length = 100, default='Mensagem')
    directed_to_student = models.BooleanField(default=True)
    state = models.CharField(max_length = 8, default = 'UNREAD',
                               choices = [("READ", "Read"), ("UNREAD", "Unread")])

    def get_absolute_url(self):
        return reverse_lazy('home')

    def __str__(self):
        return self.message
