from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

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

class StudentUpdateView(UpdateView):
    model = CustomUser
    template_name = "student_edit.html"
    # fields = ["user.student.registration"]
    fields = ["username", "email"]

class OngUpdateView(UpdateView):
    model = CustomUser
    template_name = "ong_edit.html"
    # fields = ["user.student.registration"]
    fields = ["username", "email"]
