from django.urls import path
from .views import *

urlpatterns = [
    path("create/",ProjectsCreateView.as_view(),name = "project_create"),
    path("list/",ProjectsListView.as_view(),name = "project_list"),
    path("<int:pk>/detail", ProjectsDetailView.as_view(), name="project_detail"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("<int:pk>/edit/", ProjectUpdateView.as_view(), name="project_edit"),
    path("<int:pk>/joblist/", JobListView.as_view(), name="job_list"),
    path("<int:pk>/createjob/", JobCreateView.as_view(), name="job_create"),
    path("<int:pk>/jobdetail/", JobDetailView.as_view(), name="job_detail"),
    path("<int:pk>/jobedit/", JobUpdateView.as_view(), name="job_edit"),
    path("<int:pk>/apply/", JobApplyView.as_view(), name="job_apply"),
    path("notifications/", NotificationListView.as_view(), name="notification_list"),
    path("<int:pk>/accept_deny", JobAcceptDenyView.as_view(), name="job_accept_deny"),
    path("<int:pk>/delete_notification/", NotificationDeleteView.as_view(), name="delete_notification"),
    path("<int:pk1>/<int:pk2>/dismiss_user/", JobDismissView.as_view(), name="dismiss_user"),
]
