from unittest.mock import MagicMock, patch

from azure.storage.blob import ContainerClient
from django.test import TestCase, Client
from django.contrib.auth.models import User

from quiz.models import Question, Quiz, Map


class DashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@mail.com", "test")
        f = open("spain_provincia.geojson")
        map = Map.objects.create(
            name="Provincias de España",
            content=f.read(),
            license="Creative Commons 4.0 BY",
            language="en",
        )
        f.close()
        quiz = Quiz.objects.create(
            slug="provincias",
            name="Provincias",
            author=self.user,
            description="Quiz de las provincias de España",
            map=map,
        )
        Question.objects.create(
            quiz=quiz, question="¿Dónde está Burgos?", answer="burgos"
        )
        Question.objects.create(
            quiz=quiz, question="¿Dónde está Soria?", answer="soria"
        )

    def test_show_dashboard(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="primary-action-button" href="/dashboard/create/">Create new mapaquiz</a>',
            html=True,
        )
        self.assertContains(
            response, '<a href="/quiz/provincias/">Provincias</a>', html=True
        )

    def test_show_delete_quiz(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/dashboard/delete/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete "Provincias"?')

    def test_delete_quiz_ok(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.post("/dashboard/delete/1/")
        self.assertEqual(response.status_code, 302)
        response = c.get("/dashboard/")
        self.assertNotContains(
            response, '<a href="/quiz/provincias/">Provincias</a>', html=True
        )

    def test_delete_quiz_fail(self):
        c = Client()
        c.login(username="test", password="test")
        with self.assertRaises(Quiz.DoesNotExist):
            c.post("/dashboard/delete/456/")

    def test_remix_ok(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/dashboard/remix/1/")
        self.assertEqual(response.status_code, 302)
        response = c.get("/dashboard/")
        self.assertContains(response, "Provincias Remix")


class EditorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@mail.com", "test")
        f = open("spain_provincia.geojson")
        map = Map.objects.create(
            name="Provincias de España",
            content=f.read(),
            license="Creative Commons 4.0 BY",
            language="en",
        )
        f.close()
        quiz = Quiz.objects.create(
            slug="provincias",
            name="Provincias",
            author=self.user,
            description="Quiz de las provincias de España",
            map=map,
        )
        Question.objects.create(
            quiz=quiz, question="¿Dónde está Burgos?", answer="burgos"
        )
        Question.objects.create(
            quiz=quiz, question="¿Dónde está Soria?", answer="soria"
        )

    def test_show_editor(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/editor/provincias/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mapaquiz "Provincias"')
        self.assertContains(response, '<div id="editor-map"></div>', html=True)
        self.assertContains(response, "¿Dónde está Soria?")

    def test_publish_no_settings(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/")
        self.assertNotContains(response, "Provincias")
        response = c.get("/editor/publish/1/")
        self.assertEqual(response.status_code, 412)

    @patch("editor.upload.ContainerClient", autospec=True)
    def test_publish(self, MockContainerClient):
        instance = MockContainerClient.from_container_url("")
        instance.return_value = instance

        c = Client()
        c.login(username="test", password="test")
        response = c.get("/")
        self.assertNotContains(response, "Provincias")
        response = c.post(
            "/editor/settings/1/", {"front_image": open("mapaly.png", "rb")}
        )
        assert response.status_code == 302
        response = c.get("/editor/publish/1/")
        self.assertEqual(response.status_code, 302)
        response = c.get("/")
        self.assertContains(response, "Provincias")

    def test_add_question(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.post(
            "/editor/provincias/",
            {"question": "¿Dónde está Cuenca?", "answer": "cuenca"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Dónde está Cuenca?")

    def test_remove_question(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get("/editor/question/1/")
        self.assertEqual(response.status_code, 302)
        response = c.get("/editor/provincias/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "¿Dónde está Burgos?")

    def test_submit_settings_description(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.post(
            "/editor/settings/1/", {"description": "Descripción de un mapaquiz"}
        )
        assert response.status_code == 302
        response = c.get("/editor/provincias/")
        assert response.status_code == 200
        self.assertContains(response, "Descripción de un mapaquiz")

    @patch("editor.upload.ContainerClient", autospec=True)
    def test_submit_settings_image(self, MockContainerClient):
        instance = MockContainerClient.from_container_url("")
        instance.return_value = instance

        c = Client()
        c.login(username="test", password="test")
        response = c.post(
            "/editor/settings/1/", {"front_image": open("mapaly.png", "rb")}
        )
        assert response.status_code == 302
        response = c.get("/editor/provincias/")
        assert response.status_code == 200
        self.assertContains(response, "mapaly.png")

        instance.upload_blob.assert_called_once()

    @patch("editor.upload.ContainerClient", autospec=True)
    def test_submit_settings_both(self, MockContainerClient):
        instance = MockContainerClient.from_container_url("")
        instance.return_value = instance

        c = Client()
        c.login(username="test", password="test")
        response = c.post(
            "/editor/settings/1/",
            {
                "front_image": open("mapaly.png", "rb"),
                "description": "Descripción de un mapaquiz",
            },
        )
        assert response.status_code == 302
        response = c.get("/editor/provincias/")
        assert response.status_code == 200
        self.assertContains(response, "mapaly.png")
        self.assertContains(response, "Descripción de un mapaquiz")

        instance.upload_blob.assert_called_once()
