from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomStudentCreationForm, CustomOngCreationForm

# class SignUpView(CreateView):
#     # form_class = CustomUserCreationForm
#     # success_url = reverse_lazy('login')
#     template_name = "registration/signup.html"

class StudentSignUpView(CreateView):
    form_class = CustomStudentCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/student_signup.html"

class OngSignUpView(CreateView):
    form_class = CustomOngCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/ong_signup.html"
