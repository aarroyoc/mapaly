import time

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from quiz.models import Question, Quiz, Map
from mapaly.testing import get_selenium_browser


class QuizTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user("test", "test@mail.com", "test")
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

    def test_profile_page(self):
        c = Client()
        response = c.get("/profile/test/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Provincias")

    def test_profile_nonexistant(self):
        c = Client()
        response = c.get("/profile/non-existant/")
        self.assertEqual(response.status_code, 404)

    def test_search(self):
        c = Client()
        response = c.get("/search/?q=provincia")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Provincias")

    def test_search_description(self):
        c = Client()
        response = c.get("/search/?q=españa")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Provincias")

    def test_search_nothing(self):
        c = Client()
        response = c.get("/search/?q=inexistente")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Provincias")


class QuizBrowserTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = get_selenium_browser()
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

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get(self.live_server_url)
        assert "Mapaquiz" in self.browser.title

        self.browser.find_element_by_link_text("Provincias")
        assert True

    def test_quiz_page(self):
        self.browser.get(self.live_server_url)
        quiz_link = self.browser.find_element_by_link_text("Provincias")
        quiz_link.click()

        WebDriverWait(self.browser, 10).until(expected_conditions.title_contains("Mapaquiz"))

        assert f"{self.live_server_url}/quiz/provincias/" == self.browser.current_url

    def test_timer(self):
        self.browser.get(f"{self.live_server_url}/quiz/provincias/")
        WebDriverWait(self.browser, 10).until(expected_conditions.text_to_be_present_in_element((By.ID, "time-string"), "0:05"))

    def test_click_correct_province(self):
        self.browser.get(f"{self.live_server_url}/quiz/provincias/")
        self.browser.implicitly_wait(10)
        map = self.browser.find_element_by_id("map")
        WebDriverWait(self.browser, 30).until(expected_conditions.text_to_be_present_in_element((By.ID, "question"), "¿Dónde está"))
        question = self.browser.find_element_by_id("question")
        action = ActionChains(self.browser)
        question1 = str(question.text)
        if question1 == "¿Dónde está Burgos?":
            action.move_to_element_with_offset(map, 505, 142)
        else:
            action.move_to_element_with_offset(map, 555, 190)
        action.click()
        action.perform()
        score = self.browser.find_element_by_id("points")
        self.assertEqual(int(score.text), 25)
        self.assertNotEqual(question1, question.text)

    def test_click_incorrect_province(self):
        self.browser.get(f"{self.live_server_url}/quiz/provincias/")
        self.browser.implicitly_wait(10)
        map = self.browser.find_element_by_id("map")
        WebDriverWait(self.browser, 30).until(expected_conditions.text_to_be_present_in_element((By.ID, "question"), "¿Dónde está"))
        question = self.browser.find_element_by_id("question")
        action = ActionChains(self.browser)
        action.move_to_element_with_offset(map, 400, 400)
        action.click()
        action.perform()
        score = self.browser.find_element_by_id("points")
        self.assertEqual(int(score.text), 0)
        question2 = self.browser.find_element_by_id("question")
        self.assertEqual(question.text, question2.text)

    def test_click_correct_then_incorrect(self):
        self.browser.get(f"{self.live_server_url}/quiz/provincias/")
        self.browser.implicitly_wait(10)
        map = self.browser.find_element_by_id("map")
        WebDriverWait(self.browser, 30).until(expected_conditions.text_to_be_present_in_element((By.ID, "question"), "¿Dónde está"))
        question = self.browser.find_element_by_id("question")
        action = ActionChains(self.browser)
        question1 = str(question.text)
        if question1 == "¿Dónde está Burgos?":
            action.move_to_element_with_offset(map, 505, 142)
        else:
            action.move_to_element_with_offset(map, 555, 190)
        action.click()
        action.perform()
        action = ActionChains(self.browser)
        action.move_to_element_with_offset(map, 400, 400)
        action.click()
        action.perform()
        score = self.browser.find_element_by_id("points")
        self.assertEqual(int(score.text), 15)
