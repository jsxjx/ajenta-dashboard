from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label='Keep me logged in', required=False)


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")

        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
        except User.DoesNotExist:
            user = None

        if user is not None:
            raise forms.ValidationError('Username already in use.')

        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'password')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        if self.cleaned_data.get('new_password') != self.cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")
        return self.cleaned_data
