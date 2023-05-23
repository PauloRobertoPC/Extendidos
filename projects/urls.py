from django.urls import path
from .views import *

urlpatterns = [
    path("create/",ProjectsCreateView.as_view(),name = "project_create"),
    path("list/",ProjectsListView.as_view(),name = "project_list"),
    path("<int:pk>/detail", ProjectsDetailView.as_view(), name="project_detail"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_edit"),
]
