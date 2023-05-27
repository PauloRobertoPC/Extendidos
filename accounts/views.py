from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View

from .models import CustomUser
from .forms import CustomStudentCreationForm, CustomOngCreationForm, CommentForm
from .utils import universities

class UserLoginSignUpView(View):
    template_name = 'home.html'

    def get(self, request):
        login_form = AuthenticationForm()
        student_form = CustomStudentCreationForm()
        ong_form = CustomOngCreationForm()

        return render(request, self.template_name, {
            'login_form': login_form,
            'student_form': student_form,
            'ong_form': ong_form,
        })

    def post(self, request):
        login_form = AuthenticationForm(request, data=request.POST)
        student_form = CustomStudentCreationForm(request.POST)
        ong_form = CustomOngCreationForm(request.POST)

        if login_form.is_valid() and 'user_login' in request.POST:
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        elif student_form.is_valid() and 'student_signup' in request.POST:
            student = student_form.save()
            login(request, student)
            return redirect('home')
        elif ong_form.is_valid() and 'ong_signup' in request.POST:
            ong = ong_form.save()
            login(request, ong)
            return redirect('home')

        return render(request, self.template_name, {
            'login_form': login_form,
            'student_form': student_form,
            'ong_form': ong_form,
        })

class UserDetailView(FormView):
    model = CustomUser
    form_class = CommentForm

    template_name = "urd_user/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = CustomUser.objects.get(pk=self.kwargs.get('pk'))
        context["form"] = CommentForm()
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.user = CustomUser.objects.get(pk=self.kwargs.get("pk"))
        if(comment.user != comment.author):
            comment.user.sum_avaliation += comment.stars 
            comment.user.total_avaliation += 1
            comment.user.save()
            comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_detail", kwargs={"pk": self.kwargs.get("pk")})

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'urd_user/student_edit.html'
    fields = ['cover', 'perfil', 'username', 'email', 'description'] # CustomUser fields that you wanna edit

    # Student Fields that you wanna edit
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registration'] = forms.CharField(
            widget=forms.TextInput,
            initial=self.object.student.registration,
            label='Registration'
        )
        form.fields['university'] = forms.ChoiceField(
            choices=universities,
            initial=self.object.student.university,
            label='University'
        )
        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        student = user.student
        student.registration = form.cleaned_data['registration']
        student.university = form.cleaned_data['university']
        student.save()
        return super().form_valid(form)

class OngUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "urd_user/ong_edit.html"
    fields = ['cover', 'perfil', 'username', 'email', 'description'] # CustomUser fields that you wanna edit

    # ONG Fields that you wanna edit
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cnpj'] = forms.CharField(
            widget=forms.TextInput,
            initial=self.object.ong.cnpj,
            label='CNPJ'
        )
        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        ong = user.ong
        ong.cnpj = form.cleaned_data['cnpj']
        ong.save()
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "urd_user/user_delete.html"
    success_url = reverse_lazy("home")
    
