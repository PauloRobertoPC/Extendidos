from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

from .models import CustomUser
from .forms import CustomStudentCreationForm, CustomOngCreationForm, CommentForm
from .utils import universities

class UserSignUpView(CreateView):
    form_class = CustomStudentCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_form'] = CustomStudentCreationForm()
        context['ong_form'] = CustomOngCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        if 'student_signup' in request.POST:
            self.form_class = CustomStudentCreationForm
        elif 'ong_signup' in request.POST:
            self.form_class = CustomOngCreationForm
        return super().post(request, *args, **kwargs)

class StudentSignUpView(CreateView):
    form_class = CustomStudentCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/student_signup.html"

class OngSignUpView(CreateView):
    form_class = CustomOngCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/ong_signup.html"

class UserDetailView(FormView):
    model = CustomUser
    form_class = CommentForm
    
    template_name = "urd_user/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = CustomUser.objects.get(pk=self.kwargs.get('pk'))
        context["form"] = CommentForm()
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.user = CustomUser.objects.get(pk=self.kwargs.get("pk"))
        if(comment.user != comment.author):
            comment.user.sum_avaliation += comment.stars 
            comment.user.total_avaliation += 1
            comment.user.save()
            comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("user_detail", kwargs={"pk": self.kwargs.get("pk")})

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'urd_user/student_edit.html'
    fields = ['cover', 'perfil', 'username', 'email', 'description'] # CustomUser fields that you wanna edit

    # Student Fields that you wanna edit
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['registration'] = forms.CharField(
            widget=forms.TextInput,
            initial=self.object.student.registration,
            label='Registration'
        )
        form.fields['university'] = forms.ChoiceField(
            choices=universities,
            initial=self.object.student.university,
            label='University'
        )
        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        student = user.student
        student.registration = form.cleaned_data['registration']
        student.university = form.cleaned_data['university']
        student.save()
        return super().form_valid(form)

class OngUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "urd_user/ong_edit.html"
    fields = ['cover', 'perfil', 'username', 'email', 'description'] # CustomUser fields that you wanna edit

    # ONG Fields that you wanna edit
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['cnpj'] = forms.CharField(
            widget=forms.TextInput,
            initial=self.object.ong.cnpj,
            label='CNPJ'
        )
        return form

    def form_valid(self, form):
        user = form.save(commit=False)
        ong = user.ong
        ong.cnpj = form.cleaned_data['cnpj']
        ong.save()
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "urd_user/user_delete.html"
    success_url = reverse_lazy("home")
    
