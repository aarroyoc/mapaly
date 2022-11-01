from django.test import TestCase, Client
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.username = "test"
        self.password = "test1234"
        self.email = "test@gmail.com"
        User.objects.create_user(self.username, self.email, self.password)

    def test_login_get(self):
        c = Client()
        response = c.get("/users/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_post_ok(self):
        c = Client()
        response = c.post(
            "/users/login/", {"username": self.username, "password": self.password}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_post_non_existing_user(self):
        c = Client()
        response = c.post(
            "/users/login/",
            {"username": self.username + "67", "password": self.password},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["error_messages"]), 1)
        self.assertEqual(
            response.context["error_messages"][0], "Usuario y/o contraseña erróneos"
        )

    def test_login_post_invalid_password(self):
        c = Client()
        response = c.post(
            "/users/login/",
            {"username": self.username, "password": self.password + "67"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["error_messages"]), 1)
        self.assertEqual(
            response.context["error_messages"][0], "Usuario y/o contraseña erróneos"
        )

    def test_register_get(self):
        c = Client()
        response = c.get("/users/register/")
        self.assertEqual(response.status_code, 200)

    def test_register_post_ok(self):
        c = Client()
        response = c.post(
            "/users/register/",
            {
                "username": self.username + "42",
                "password": self.password,
                "email": self.email,
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_register_post_already_existing(self):
        c = Client()
        response = c.post(
            "/users/register/",
            {"username": self.username, "password": self.password, "email": self.email},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["error_messages"]), 1)

    def test_register_post_empty_email(self):
        c = Client()
        response = c.post(
            "/users/register/",
            {"username": self.username + "27", "password": self.password, "email": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["error_messages"]), 1)
