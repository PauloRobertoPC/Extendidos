from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import Project,Job


class ProjectsCreateView(LoginRequiredMixin,CreateView):
    model = Project
    template_name = 'project_create.html'
    fields = ['title', 'description', 'location']

    def form_valid(self,form):
        form.instance.ong = self.request.user.ong
        return super().form_valid(form)
    

    
class ProjectsDetailView(LoginRequiredMixin,ListV):
    model = Project
    template_name = "project_detail.html"



class JobCreateView(LoginRequiredMixin,CreateView):
    model = Job
    template_name = 'job_create.html'
    fields = ['title','description','location','available_vacancies','job_begin','job_end']

    def form_valid(self,form):
        form.instance.ong = self.request.user.ong
        return super().form_valid(form)
    







# Create your views here.
