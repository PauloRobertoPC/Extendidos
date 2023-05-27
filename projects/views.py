from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project,Job,Notification
from django.db.models import Q
from accounts.models import CustomUser

class ProjectsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    template_name = 'project/project_create.html'
    fields = ['title', 'description', 'location',]

    def form_valid(self,form):
        form.instance.ong = self.request.user.ong
        return super().form_valid(form)

    def test_func(self):
        obj = self.request.user
        return obj.is_ong

class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "project/project_list.html"

class ProjectsDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "project/project_detail.html"

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "project/project_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        project = self.get_object()
        return project.ong.user == self.request.user

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'project/project_edit.html'
    fields = ['title', 'description', 'location']

    def test_func(self):
        project = self.get_object()
        return project.ong.user == self.request.user

class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    template_name = 'job/job_create.html'
    fields = ['title','description','location','available_vacancies', 'is_active', 'job_begin','job_end']

    def form_valid(self,form):
        form.instance.project = Project.objects.get(pk = self.kwargs['pk']) 
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        return job.project.ong.user == self.request.user

class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "job/job_list.html"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Job.objects.filter(project=pk)

class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = "job/job_detail.html"

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'job/job_edit.html'
    fields = ['title','description','location','available_vacancies', 'is_active', 'job_begin','job_end']

    def test_func(self):
        job = self.get_object()
        return job.project.ong.user == self.request.user

class JobApplyView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Notification
    template_name = 'job/job_apply.html'

    def get(self, request, *args, **kwargs):
        job = Job.objects.get(pk = self.kwargs.get('pk'))
        student = request.user.student
        messageArg = "O estudante '" + request.user.username + "' está se candidatando ao trabalho '" + job.title + "' do projeto '" + job.project.title + "'."
        Notification.objects.create(student = student, job = job, message=messageArg, directed_to_student=False)
        return redirect('home')

    def post(self, request, *args, **kwargs):
       return redirect('home')

    def test_func(self):
        user = self.request.user 
        job = Job.objects.get(pk = self.kwargs.get('pk'))
        # Only students can apply to the job
        check1 = user.is_student == True
        if not check1:
            return False
        #The student can apply to this only with he is not in the job
        queryset_job = job.student.filter(pk=user.student.pk)
        check2 = not queryset_job.exists()
        # The student can't aplly to the job if he's waiting the ong answer the notification
        queryset_notification = Notification.objects.filter(student=user.student, job=job, directed_to_student=False)
        check3 = not queryset_notification.exists() 
        return  check2 and check3

class JobAcceptDenyView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Notification
    template_name = 'job/job_accept_deny.html'

    def get(self, request, *args, **kwargs):
        operation = int(self.request.GET.get("operation"))
        notification = Notification.objects.get(pk=self.kwargs.get('pk'))
        job = notification.job
        messageArg = ""
        if(operation):
            job.available_vacancies -= 1;
            job.student.add(notification.student)
            job.save()
            messageArg = "A sua candidatura para o trabalho '" +job.title+  "' do projeto '" +job.project.title+ "' foi aceita!"
        else:
            messageArg = "A sua candidatura para o trabalho '" +job.title+  "' do projeto '" +job.project.title+ "' foi negada!"
        notification.directed_to_student = True
        notification.message = messageArg
        notification.save()
        return redirect('notification_list')

    def post(self, request, *args, **kwargs):
       return redirect('home')

    def test_func(self):
        user = self.request.user
        notification = self.get_object()
        return user.is_ong and notification.job.project.ong == user.ong

class JobDismissView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'job/dismiss_user.html'
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        job_pk=self.kwargs.get('pk1')
        student_pk = self.kwargs.get('pk2')
        job = Job.objects.get(pk=job_pk)
        student = CustomUser.objects.get(pk=student_pk).student
        job.student.remove(student)
        job.save()
        messageArg = "A sua candidatura para o trabalho '" +job.title+  "' do projeto '" +job.project.title+ "' foi removida!"
        Notification.objects.create(student = student, job = job, message=messageArg)
        return redirect('home')

    def test_func(self):
        job_pk=self.kwargs.get('pk1')
        job = Job.objects.get(pk=job_pk)
        return job.project.ong.user == self.request.user

class NotificationListView(LoginRequiredMixin,ListView):
    model = Notification
    template_name = "notification/notification_list.html"

    def get_queryset(self):
        user = self.request.user
        if(user.is_ong):
            return Notification.objects.filter(
                Q(state='UNREAD'),
                Q(job__project__ong=self.request.user.ong),
                Q(directed_to_student=False)
            )
        return Notification.objects.filter(
            Q(state='UNREAD'),
            Q(student__user=user),
            Q(directed_to_student=True)
        )

class NotificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Notification
    template_name = 'notification/notification_delete.html'
    success_url = reverse_lazy("notification_list")

    def test_func(self):
        notification = self.get_object()
        user = self.request.user
        if(user.is_ong):
            return False
        return notification.student == user.student
