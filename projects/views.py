from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project,Job

class ProjectsCreateView(LoginRequiredMixin,CreateView):
    model = Project
    template_name = 'project_create.html'
    fields = ['title', 'description', 'location',]

    def form_valid(self,form):
        form.instance.ong = self.request.user.ong
        return super().form_valid(form)

class ProjectsListView(LoginRequiredMixin,ListView):
    model = Project
    template_name = "project_list.html"

class ProjectsDetailView(LoginRequiredMixin,DetailView):
    model = Project
    template_name = "project_detail.html"

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "project_delete.html"
    success_url = reverse_lazy("home")

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_edit.html'
    fields = ['title', 'description', 'location']

class JobListView(LoginRequiredMixin,ListView):
    model = Job
    template_name = "job_list.html"

class JobCreateView(LoginRequiredMixin,CreateView):
    model = Job
    template_name = 'job_create.html'
    fields = ['title','description','location','available_vacancies','job_begin','job_end']

    def form_valid(self,form):
        form.instance.project = Project.objects.get(pk = self.kwargs['pk']) 
        return super().form_valid(form)
