from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username='staff', password='test-password', is_staff=True
        )
        self.regular_user = get_user_model().objects.create_user(
            username='regular', password='test-password'
        )

    def test_staff_pages_redirect_anonymous_visitors_to_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('dashboard')}"
        )

    def test_authenticated_non_staff_user_is_forbidden(self):
        self.client.force_login(self.regular_user)
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 403)

    def test_staff_can_log_in_and_log_out(self):
        response = self.client.post(reverse('login'), {
            'username': 'staff',
            'password': 'test-password',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 200)

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertRedirects(
            self.client.get(reverse('dashboard')),
            f"{reverse('login')}?next={reverse('dashboard')}",
        )
