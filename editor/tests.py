from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User

from editor.views import DashboardView
from quiz.models import Question, Quiz, Map

class DashboardTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user("test", "test@mail.com", "test")
        f = open("spain_provincia.geojson")
        map = Map.objects.create(
            name="Provincias de España",
            content=f.read(),
            license="Creative Commons 4.0 BY"
        )
        f.close()
        quiz = Quiz.objects.create(
            slug="provincias",
            name="Provincias",
            author=self.user,
            description="Quiz de las provincias de España",
            map=map
        )
        Question.objects.create(
            quiz=quiz,
            question="¿Dónde está Burgos?",
            answer="burgos"
        )
        Question.objects.create(
            quiz=quiz,
            question="¿Dónde está Soria?",
            answer="soria"
        )

    def test_show_dashboard(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a class="primary-action-button" href="/dashboard/create/">Crear nuevo quiz</a>', html=True)
        self.assertContains(response, '<a href="/quiz/provincias/">Provincias</a>', html=True)

    def test_show_delete_quiz(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/dashboard/delete/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '¿Estás seguro que deseas borrar el quiz "Provincias"?')

    def test_delete_quiz_ok(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.post("/dashboard/delete/1/")
        self.assertEqual(response.status_code, 302)
        response = c.get("/dashboard/")
        self.assertNotContains(response, '<a href="/quiz/provincias/">Provincias</a>', html=True)


    def test_delete_quiz_fail(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.post("/dashboard/delete/456/")
        self.assertEqual(response.status_code, 302)
        response = c.get("/dashboard/")
        self.assertContains(response, '<a href="/quiz/provincias/">Provincias</a>', html=True)

    def test_remix_ok(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/dashboard/remix/1/")
        self.assertEqual(response.status_code, 302)
        response = c.get("/dashboard/")
        self.assertContains(response, 'Provincias Remix')
