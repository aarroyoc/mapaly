from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

from users.forms import LoginForm, RegisterForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()

        context = {"form": form}
        return render(request, "users/login.html", context)

    def post(self, request):
        error_messages = []
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is None:
                error_messages.append("Usuario y/o contraseña erróneos")
            else:
                login(request, user)
                return redirect(request.GET.get("next", "home"))
        else:
            for error in form.errors:
                msg = form.errors[error]
                error_messages.append(f"{error}: {msg}")
        context = {"form": form, "error_messages": error_messages}
        return render(request, "users/login.html", context)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("home")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()

        context = {"form": form}
        return render(request, "users/register.html", context)

    def post(self, request):
        error_messages = []
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                User.objects.create_user(username, email, password)
                return redirect("home")
            except Exception as exp:
                error_messages.append(exp.args[0])
        else:
            for error in form.errors:
                msg = form.errors[error]
                error_messages.append(f"{error}: {msg}")
        context = {
            "form": form,
            "error_messages": error_messages,
        }
        return render(request, "users/register.html", context)
