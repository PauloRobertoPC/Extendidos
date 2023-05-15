from django.urls import path
from django.views.generic.base import TemplateView
from .views import StudentSignUpView, OngSignUpView

urlpatterns = [
    path("signup/", TemplateView.as_view(template_name="../templates/registration/signup.html"), name="signup"),
    path("student_singup/", StudentSignUpView.as_view(), name="student_signup"),
    path("ong_singup/", OngSignUpView.as_view(), name="ong_signup"),
]
