from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    StudentSignUpView, 
    OngSignUpView, 
    UserDetailView,
    StudentUpdateView, 
    OngUpdateView,
    UserDeleteView
)

urlpatterns = [
    path("student/<int:pk>/edit/", StudentUpdateView.as_view(), name="student_edit"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("ong/<int:pk>/edit/", OngUpdateView.as_view(), name="ong_edit"),
    path("user/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    path("signup/", TemplateView.as_view(template_name="../templates/registration/signup.html"), name="signup"),
    path("student_singup/", StudentSignUpView.as_view(), name="student_signup"),
    path("ong_singup/", OngSignUpView.as_view(), name="ong_signup"),
]
