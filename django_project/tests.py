from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

class HomePageTests(TestCase):
    def test_url_exists_at_correct_location_signupview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")
        self.assertEqual(response.status_code, 200)
