from django.shortcuts import redirect
from django import forms
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, Job, Notification, Tag
from django.db.models import Q
from accounts.models import CustomUser

class ProjectsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    template_name = 'project/project_create.html'
    fields = ['title', 'description', 'location',]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
        form.fields['tags'] = tags
        form.fields['title'].label = "Título"
        form.fields['location'].label = "Localização"
        form.fields['description'].label = "Descrição"
        return form

    def form_valid(self, form):
        form.instance.ong = self.request.user.ong
        project = form.save(commit=False)
        project.save()
        selected_tags = form.cleaned_data.get('tags')
        for tag in selected_tags:
            tag.project.add(project)
        return super().form_valid(form)

    def test_func(self):
        obj = self.request.user
        return obj.is_ong

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

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
    fields = ['title', 'description', 'location', 'cover',]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        project = self.get_object()
        print(project)
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
        selected_tags = project.tag_set.all()
        form.fields['tags'] = tags
        form.fields['tags'].initial = selected_tags
        return form

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        selected_tags = form.cleaned_data.get('tags')
        for tag in selected_tags:
            tag.project.add(project)
        return super().form_valid(form)


    def test_func(self):
        project = self.get_object()
        return project.ong.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    template_name = 'job/job_create.html'
    fields = ['title','description','location','available_vacancies', 'is_active', 'job_begin','job_end']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
        form.fields['tags'] = tags
        form.fields['title'].label = "Título"
        form.fields['location'].label = "Localização"
        form.fields['description'].label = "Descrição"
        form.fields['available_vacancies'].label = "Total de Vagas Disponíveis"
        form.fields['is_active'].label = "Está Acontecendo"
        form.fields['job_begin'].label = "Data de Início"
        form.fields['job_end'].label = "Data Final"
        return form

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk = self.kwargs['pk']) 
        job = form.save(commit=False)
        job.save()
        selected_tags = form.cleaned_data.get('tags')
        for tag in selected_tags:
            tag.job.add(job)
        return super().form_valid(form)

    def test_func(self):
        pk = self.kwargs.get("pk")
        project = Project.objects.get(pk=pk)
        return project.ong.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.pk})


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "job/job_list.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
        form.fields['tags'] = tags
        return form

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk = self.kwargs['pk']) 
        job = form.save(commit=False)
        job.save()
        selected_tags = form.cleaned_data.get('tags')
        for tag in selected_tags:
            tag.job.add(job)
        return super().form_valid(form)

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Job.objects.filter(project=pk)

class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = "job/job_detail.html"

    # Using the method below to calculate 'notification_received', that is 
    # true if the student already apply to the job
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # if the user is a ong the context is the normal
        if user.is_ong:
            return context

        student = user.student
        job = Job.objects.get(pk=self.kwargs.get('pk'))
        notification_received = Notification.objects.filter(student=student, job=job, directed_to_student=False).exists()
        context['notification_received'] = notification_received

        return context

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    template_name = 'job/job_edit.html'
    fields = ['title', 'description', 'cover', 'location', 'available_vacancies', 'is_active', 'job_begin', 'job_end']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        job = self.get_object()
        tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
        selected_tags = job.tag_set.all()
        form.fields['tags'] = tags
        form.fields['tags'].initial = selected_tags
        form.fields['title'].label = "Título"
        form.fields['location'].label = "Localização"
        form.fields['description'].label = "Descrição"
        form.fields['available_vacancies'].label = "Total de Vagas Disponíveis"
        form.fields['is_active'].label = "Está Acontecendo"
        form.fields['job_begin'].label = "Data de Início"
        form.fields['job_end'].label = "Data Final"
        form.fields['cover'].label = "Foto de Capa"
        return form

    def form_valid(self, form):
        job = form.save(commit=False)
        job.save()
        selected_tags = form.cleaned_data.get('tags')
        for tag in selected_tags:
            tag.job.add(job)
        return super().form_valid(form)

    def test_func(self):
        job = self.get_object()
        return job.project.ong.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.pk})

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = "job/job_delete.html"
    success_url = reverse_lazy("home")

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
        return redirect("job_detail", pk=job.pk)

    def post(self, request, *args, **kwargs):
       return redirect('home')

    def test_func(self):
        user = self.request.user 
        job = Job.objects.get(pk = self.kwargs.get('pk'))
        # Only students can apply to the job
        check1 = user.is_student == True
        if not check1:
            return False
        #The student can apply to this only when he is not in the job
        queryset_job = job.student.filter(pk=user.student.pk)
        check2 = not queryset_job.exists()
        # The student can't aplly to the job if he's waiting the ong answer the notification
        queryset_notification = Notification.objects.filter(student=user.student, job=job, directed_to_student=False)
        check3 = not queryset_notification.exists() 
        return  check2 and check3 and job.available_vacancies > 0;

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
        return redirect("job_detail", pk=job.pk)

    def post(self, request, *args, **kwargs):
       return redirect('home')

    def test_func(self):
        user = self.request.user
        notification = self.get_object()
        return user.is_ong and notification.job.project.ong == user.ong

class JobDismissView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'job/dismiss_user.html'

    def get(self, request, *args, **kwargs):
        job_pk=self.kwargs.get('pk1')
        student_pk = self.kwargs.get('pk2')
        job = Job.objects.get(pk=job_pk)
        student = CustomUser.objects.get(pk=student_pk).student
        job.student.remove(student)
        job.save()
        messageArg = "A sua candidatura para o trabalho '" +job.title+  "' do projeto '" +job.project.title+ "' foi removida!"
        Notification.objects.create(student = student, job = job, message=messageArg)
        return redirect("job_detail", pk=job.pk)

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
    success_url = reverse_lazy("home")

    def test_func(self):
        notification = self.get_object()
        user = self.request.user
        if(user.is_ong):
            return False
        return notification.student == user.student

class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tag
    template_name = 'tag/tag_create.html'
    fields = ["tag_name"]
    success_url = reverse_lazy("tag_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tag_name'].label = "Nome da Tag"
        return form

    def test_func(self):
        return True

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "tag/tag_list.html"

class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = "tag/tag_delete.html"
    success_url = reverse_lazy("tag_list")

    def test_func(self):
        return True

class ProjectTagListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/project_tag_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tags'] = self.request.GET.getlist('tags[]')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        selected_tags = self.request.GET.getlist('tags[]')
        if selected_tags:
            queryset = queryset.filter(tag__tag_name__in=selected_tags)

        return queryset

class JobTagListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'job/job_tag_list.html'
    context_object_name = 'jobs'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tags'] = self.request.GET.getlist('tags[]')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        selected_tags = self.request.GET.getlist('tags[]')
        if selected_tags:
            queryset = queryset.filter(tag__tag_name__in=selected_tags)

        return queryset
