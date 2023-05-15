from django.urls import path
from django.views.generic.base import TemplateView
from .views import StudentSignUpView, OngSignUpView, StudentDetailView, OngDetailView

urlpatterns = [
    path("student/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path("ong/<int:pk>/", OngDetailView.as_view(), name="ong_detail"),
    path("signup/", TemplateView.as_view(template_name="../templates/registration/signup.html"), name="signup"),
    path("student_singup/", StudentSignUpView.as_view(), name="student_signup"),
    path("ong_singup/", OngSignUpView.as_view(), name="ong_signup"),
]
