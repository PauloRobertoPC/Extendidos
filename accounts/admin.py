from django.contrib import admin
from .models import CustomUser, Student, Ong, Comment

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Ong)
admin.site.register(Comment)
