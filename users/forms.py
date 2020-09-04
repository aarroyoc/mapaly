from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    username = forms.CharField(label="Usuario")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("email"):
            self.add_error("email", "Email should not be empty")
