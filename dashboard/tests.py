from datetime import date, timedelta
from random import randint

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.contrib import auth

from .forms import UserForm


class TestUserWithoutPermission(TestCase):
    """Test when the user does not have the can_view_stats permission. A 403 error code should be returned."""

    def setUp(self):
        User.objects.create_user(username='temp', password='temp')
        self.client.login(username='temp', password='temp')

    def test_is_authenticated(self):
        user = auth.get_user(self.client)
        assert user.is_authenticated()

    def test_user_stats(self):
        response = self.client.post('/user-stats/')
        self.assertEqual(response.status_code, 403)

    def test_room_stats(self):
        response = self.client.post('/room-stats/')
        self.assertEqual(response.status_code, 403)

    def test_calls_per_day(self):
        response = self.client.post('/calls-per-day/')
        self.assertEqual(response.status_code, 403)

    def test_concurrent_lines(self):
        response = self.client.post('/concurrent-lines/')
        self.assertEqual(response.status_code, 403)

    def test_platform_stats(self):
        response = self.client.post('/platform-stats/')
        self.assertEqual(response.status_code, 403)

    def test_os_stats(self):
        response = self.client.post('/os-stats/')
        self.assertEqual(response.status_code, 403)

    def test_calls_by_country(self):
        response = self.client.post('/calls-by-country/')
        self.assertEqual(response.status_code, 403)


class TestUserWithPermissionNoSessionVariables(TestCase):
    """
    Test when the user has the can_view_stats permission, but the session variables are empty.
    This happens if the user types directly the URL skipping the index page form.
    In that case, the user should be redirected to the index page,
    or to the login page for the tenant-specific view functions.
    """

    def setUp(self):
        User.objects.create_user(username='temp', password='temp')
        self.client.login(username='temp', password='temp')

        user = auth.get_user(self.client)
        user.user_permissions.add(Permission.objects.get(codename='can_view_stats'))

    def test_user_stats(self):
        response = self.client.post('/user-stats/')
        self.assertRedirects(response, '/')

    def test_room_stats(self):
        response = self.client.post('/room-stats/')
        self.assertRedirects(response, '/')

    def test_calls_per_day(self):
        response = self.client.post('/calls-per-day/')
        self.assertRedirects(response, '/')

    def test_concurrent_lines(self):
        response = self.client.post('/concurrent-lines/')
        self.assertRedirects(response, '/')

    def test_platform_stats(self):
        response = self.client.post('/platform-stats/')
        self.assertRedirects(response, '/')

    def test_os_stats(self):
        response = self.client.post('/os-stats/')
        self.assertRedirects(response, '/')

    def test_calls_by_country(self):
        response = self.client.post('/calls-by-country/')
        self.assertRedirects(response, '/auth/login/?next=/calls-by-country/')

    def test_cdr_report(self):
        response = self.client.post('/cdr/')
        self.assertRedirects(response, '/auth/login/?next=/cdr/')


class TestUserWithPermission(TestCase):
    """Test when the user has the can_view_stats permission and the session variables have right values."""

    def setUp(self):
        User.objects.create_user(username='temp', password='temp')
        self.client.login(username='temp', password='temp')

        user = auth.get_user(self.client)
        user.user_permissions.add(Permission.objects.get(codename='can_view_stats'))

        session = self.client.session
        session['username'] = user.username
        session['selected_db'] = 'platformc'
        session['start_date'] = (date.today() - timedelta(30)).strftime('%d/%m/%Y')
        session['end_date'] = date.today().strftime('%d/%m/%Y')
        session.save()

    def test_user_stats(self):
        response = self.client.post('/user-stats/')
        self.assertEqual(response.status_code, 200)

    def test_room_stats(self):
        response = self.client.post('/room-stats/')
        self.assertEqual(response.status_code, 200)

    def test_calls_per_day(self):
        response = self.client.post('/calls-per-day/')
        self.assertEqual(response.status_code, 200)

    def test_concurrent_lines(self):
        response = self.client.post('/concurrent-lines/')
        self.assertEqual(response.status_code, 200)

    def test_platform_stats(self):
        response = self.client.post('/platform-stats/')
        self.assertEqual(response.status_code, 200)

    def test_os_stats(self):
        response = self.client.post('/os-stats/')
        self.assertEqual(response.status_code, 200)

    def test_calls_by_country(self):
        response = self.client.post('/calls-by-country/')
        self.assertRedirects(response, '/auth/login/?next=/calls-by-country/')

    def test_cdr_report(self):
        response = self.client.post('/cdr/')
        self.assertRedirects(response, '/auth/login/?next=/cdr/')


class TestUserSpecificReports(TestCase):
    """Test the two tenant-specific view functions: calls_by_country() and cdr_report()."""

    def setUp(self):
        User.objects.create_user(username='ActionAid', password='temp')
        User.objects.create_user(username='Jisc', password='temp')

        session = self.client.session
        session['selected_db'] = 'ajenta_io'
        session['start_date'] = (date.today() - timedelta(30)).strftime('%d/%m/%Y')
        session['end_date'] = date.today().strftime('%d/%m/%Y')
        session.save()

    def test_calls_by_country(self):
        self.client.login(username='ActionAid', password='temp')

        user = auth.get_user(self.client)
        user.user_permissions.add(Permission.objects.get(codename='can_view_stats'))

        session = self.client.session
        session['username'] = user.username
        session.save()

        response = self.client.post('/calls-by-country/')
        self.assertEqual(response.status_code, 200)

    def test_cdr_report(self):
        self.client.login(username='Jisc', password='temp')

        session = self.client.session
        session['username'] = 'Jisc'
        session.save()

        response = self.client.post('/cdr/')
        self.assertEqual(response.status_code, 200)


class TestForm(TestCase):
    """Test form validation."""

    def test_valid_data(self):
        form = UserForm({'start_date': date.today() - timedelta(30), 'end_date': date.today()})
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = UserForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'start_date': ['This field is required.'],
            'end_date': ['This field is required.'],
        })

    def test_invalid_past_data(self):
        random_date = date(2013, 04, 01) - timedelta(randint(1, 365))
        form = UserForm({'start_date': random_date.strftime('%d/%m/%Y'), 'end_date': date.today()})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            '__all__': ['There is no data before 01/04/2013.']
        })

    def test_invalid_future_data(self):
        form = UserForm({'start_date': date.today(), 'end_date': date.today() + timedelta(30)})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            '__all__': ['You cannot select a future date.']
        })

    def test_nonsense_data(self):
        form = UserForm({'start_date': date.today(), 'end_date': date.today() - timedelta(30)})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            '__all__': ['End date must be after start date.']
        })
