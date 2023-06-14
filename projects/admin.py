from django.contrib import admin

from .models import Project, Job, Notification, Tag

admin.site.register(Project)
admin.site.register(Job)
admin.site.register(Notification)
admin.site.register(Tag)
