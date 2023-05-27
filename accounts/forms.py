from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CustomUser, Student, Ong, Comment
from .utils import universities

class CustomStudentCreationForm(UserCreationForm):
    registration = forms.CharField(required=True)
    university = forms.ChoiceField(required=True, choices=universities)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.registration = self.cleaned_data.get('registration')
        student.university = self.cleaned_data.get('university')
        student.save()
        return user

class CustomOngCreationForm(UserCreationForm):
    cnpj = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_ong = True
        user.save()
        ong = Ong.objects.create(user=user)
        ong.cnpj = self.cleaned_data.get('cnpj')
        ong.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('stars', 'comment',)
