from django.test import TestCase

import sys
sys.path.append("..")

from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Student,CustomUser,Ong
from .models import Project


class ProjectTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(username = "testuser", email = "testuser@gmail.com",password = "passtest123")
        self.student.is_student = True

        self.user = CustomUser.objects.create_user(username = "testong", email = "testong@gmail.com",password = "passtest123")
        self.ong = Ong.objects.create(user = self.user)

        self.Proj = Project.objects.create(ong = self.ong,title = "Projeto teste", description = "Criação de uma projeto teste")
    
    def test_create_project(self):
        self.assertEqual(self.Proj.description,"Criação de uma projeto teste")
        self.assertNotEqual(self.Proj.ong,self.user)

    def test_get_detail(self):
        self.client.login(username = "testong@gmail.com",password = "passtest123")
        url = reverse('project_detail',args = [self.Proj.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_get_detail_not_logged(self):
        url = reverse('project_detail',args = [self.Proj.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)