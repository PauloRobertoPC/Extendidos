from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from .models import CustomUser
from .forms import CustomStudentCreationForm, CustomOngCreationForm
from .utils import universities

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
    template_name = "urd_user/student_detail.html"

class OngDetailView(DetailView):
    model = CustomUser
    template_name = "urd_user/ong_detail.html"

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

