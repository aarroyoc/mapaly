from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("email"):
            self.add_error("email", "Email should not be empty")
