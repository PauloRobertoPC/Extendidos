from django.urls import path
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path("create/",ProjectsCreateView.as_view(),name = "project_create")
    
]