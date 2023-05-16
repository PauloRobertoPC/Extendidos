from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from .models import CustomUser
from .forms import CustomStudentCreationForm, CustomOngCreationForm

class StudentSignUpView(CreateView):
    form_class = CustomStudentCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/student_signup.html"

class OngSignUpView(CreateView):
    form_class = CustomOngCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/ong_signup.html"

class StudentDetailView(DetailView):
    model = CustomUser
    template_name = "student_detail.html"

class OngDetailView(DetailView):
    model = CustomUser
    template_name = "ong_detail.html"

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'student_edit.html'
    fields = ['username', 'email', 'description'] # CustomUser fields that you wanna edit

    # Student Fields that you wanna edit
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registration'] = forms.CharField(
            widget=forms.TextInput,
            initial=self.object.student.registration,
            label='Registration'
        )
        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        student = user.student
        student.registration = form.cleaned_data['registration']
        student.save()
        return super().form_valid(form)

class OngUpdateView(UpdateView):
    model = CustomUser
    template_name = "ong_edit.html"
    fields = ["username", "email", 'description'] # CustomUser fields that you wanna edit

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

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = "user_delete.html"
    success_url = reverse_lazy("home")
