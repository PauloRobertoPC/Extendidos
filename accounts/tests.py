from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Student,CustomUser


class SignUpTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(username = "testuser", email = "testuser@gmail.com",password = "passtest123")
        self.student.is_student = True

        self.ong = CustomUser.objects.create_user(username = "testong", email = "testong@gmail.com",password = "passtest123")
        self.ong.is_ong = True

    def test_signup_post_student(self):
        logged = self.client.login(username = "testuser@gmail.com",password = "passtest123")
        self.assertEqual(self.student.is_student, True)
        self.assertEqual(logged, True)

    def test_signup_post_ong(self):
        logged = self.client.login(username = "testong@gmail.com",password = "passtest123")
        self.assertEqual(self.ong.is_ong, True)
        self.assertEqual(logged, True)
    
    def test_signup_post_detail_student(self):
        self.client.login(username = "testuser@gmail.com",password = "passtest123")
        url = reverse('user_detail', args=[self.student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_signup_post_detail_ong(self):
        self.client.login(username = "testong@gmail.com",password = "passtest123")
        url = reverse('user_detail', args=[self.ong.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_signup_post_detail_ong_not_logged(self):
        url = reverse('user_detail', args=[self.ong.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code,302)