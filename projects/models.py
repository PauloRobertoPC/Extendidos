from django.db import models
from accounts.models import Ong,Student
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
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, choices=states, default="Ceará")
    available_vacancies = models.IntegerField()
    job_begin =  models.DateTimeField()
    job_end = models.DateTimeField()


    def get_absolute_url(self):
        return reverse_lazy('home')


    def __str__(self):
        return self.title
