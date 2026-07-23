from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class AccountsModelAndAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='parker123',
            email='parker@example.com',
            phone='+919876543210',
            password='Password@123'
        )

    def test_custom_user_creation(self):
        self.assertEqual(self.user.username, 'parker123')
        self.assertEqual(self.user.email, 'parker@example.com')
        self.assertEqual(self.user.phone, '+919876543210')
        self.assertEqual(str(self.user), 'parker123')

    def test_login_view_status(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_status(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
