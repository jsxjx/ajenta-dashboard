from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth


class TestBeforeLogin(TestCase):
    """Tests redirections to the LOGIN_URL when the user is not logged in."""
    def setUp(self):
        User.objects.create_user(username='temp', password='temp')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.url, '/auth/login/?next=/')

    def test_change_password(self):
        response = self.client.get('/auth/change-password')
        self.assertRedirects(response, '/auth/login/?next=/auth/change-password')

    def test_create_user(self):
        response = self.client.get('/auth/create-user')
        self.assertRedirects(response, '/auth/login/?next=/auth/create-user')

    def test_login(self):
        response = self.client.post('/auth/login/', {'username': 'temp', 'password': 'temp'}, follow=True)
        self.assertRedirects(response, '/')


class TestAfterLogin(TestCase):
    """Tests redirections when the user is logged in."""
    def setUp(self):
        User.objects.create_user(username='temp', password='temp')
        self.client.login(username='temp', password='temp')

    def test_is_authenticated(self):
        user = auth.get_user(self.client)
        assert user.is_authenticated()

    def test_change_url(self):
        response = self.client.get('/auth/change-password/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.get('/auth/create-user/')
        self.assertRedirects(response, '/auth/login/?next=/auth/create-user/')

    def test_logout_url(self):
        response = self.client.get('/auth/logout/')
        self.assertRedirects(response, '/auth/login')
