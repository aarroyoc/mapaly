from django.test import TestCase, Client
from django.contrib.auth.models import User
from quiz.models import Question, Quiz, Map


class QuizTestCase(TestCase):
    def setUp(self):
        user = User.objects.create()
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
            author=user,
            description="Quiz de las provincias de España",
            map=map,
            status=Quiz.QuizStatus.PUBLISHED,
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

    def test_home_page(self):
        """Home page shows at least one link to a quiz"""
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context["page_obj"]) > 0)
        self.assertContains(response, '<a href="/quiz/provincias/">Provincias</a>', html=True)

    def test_quiz_page(self):
        """Quiz page shows a Leaflet map"""
        c = Client()
        response = c.get("/quiz/provincias/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="map"></div>', html=True)
        self.assertContains(response, '<script type="module" src="/intermap/bundle.js"></script>', html=True)

    def test_quiz_page_not_exists(self):
        """Quiz page of a non-existant quiz"""
        c = Client()
        response = c.get("/quiz/pepitos/")
        self.assertEqual(response.status_code, 404)

    def test_quiz_api(self):
        """Quiz API returns 200 for existing quiz"""
        c = Client()
        response = c.get("/api/quiz/provincias/", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)
