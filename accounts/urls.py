from django.urls import path

from .views import (
    UserDetailView,
    StudentUpdateView, 
    OngUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path("student/<int:pk>/edit/", StudentUpdateView.as_view(), name="student_edit"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("ong/<int:pk>/edit/", OngUpdateView.as_view(), name="ong_edit"),
    path("user/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
]
