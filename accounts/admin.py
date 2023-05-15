# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .forms import CustomStudentCreationForm, CustomStudentChangeForm
# from .forms import CustomOngCreationForm, CustomOngChangeForm
from .forms import CustomStudentCreationForm, CustomOngCreationForm
from .models import CustomUser, Student, Ong

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_student",
        "is_ong",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_student", "is_ong", )}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("is_student", "is_ong", )}),)
 
# class CustomStudentAdmin(UserAdmin):
#     add_form = CustomStudentCreationForm
#     form = CustomStudentChangeForm
#     model = Student
#     list_display = [
#         "email",
#         "username",
#         "registration",
#     ]
#     fieldsets =  ((None, {"fields": ("registration",)}),)
#     add_fieldsets =  ((None, {"fields": ("registration",)}),)
#
# class CustomOngAdmin(UserAdmin):
#     add_form = CustomOngCreationForm
#     form = CustomOngChangeForm
#     model = Ong
#     list_display = [
#         "email",
#         "username",
#         "cnpj",
#     ]
#     fieldsets =  ((None, {"fields": ("cnpj",)}),)
#     add_fieldsets =  ((None, {"fields": ("cnpj",)}),)

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Student, CustomStudentAdmin)
# admin.site.register(Ong, CustomOngAdmin)
admin.site.register(Student)
admin.site.register(Ong)
