"""mapaly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from quiz.views import (
    QuizView,
    HomeView,
    ProfileView,
    SearchView,
    add_comment,
    set_language,
    get_random_quiz,
)
from quiz.api import QuizDetailAPI
from users.views import LoginView, LogoutView, RegisterView
from editor.views import (
    DashboardView,
    DeleteMapView,
    EditorView,
    NewView,
    delete_question,
    publish_quiz,
    remix_quiz,
    save_quiz_settings,
)
from score.api import ScoreAPI, me
from text.views import render_page
from wizard.views import wizard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("quiz/<str:slug>/", QuizView.as_view(), name="quiz"),
    path("comments/<int:pk>/", add_comment, name="add-comment"),
    path("profile/<user>/", ProfileView.as_view(), name="profile"),
    path("search/", SearchView.as_view(), name="search"),
    path("users/login/", LoginView.as_view(), name="login"),
    path("users/logout/", LogoutView.as_view(), name="logout"),
    path("users/register/", RegisterView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("dashboard/delete/<int:pk>/", DeleteMapView.as_view(), name="delete-quiz"),
    path("dashboard/create/", NewView.as_view(), name="create-quiz"),
    path("dashboard/remix/<int:pk>/", remix_quiz, name="remix"),
    path("editor/<str:slug>/", EditorView.as_view(), name="editor"),
    path("editor/question/<int:pk>/", delete_question, name="delete-question"),
    path("editor/publish/<int:pk>/", publish_quiz, name="publish"),
    path("editor/settings/<int:pk>/", save_quiz_settings, name="save-quiz-settings"),
    path("api/quiz/<str:slug>/", QuizDetailAPI.as_view(), name="quiz_detail_api"),
    path("api/score/<str:slug>/", ScoreAPI.as_view(), name="score-api"),
    path("api/me/", me, name="me"),
    path("text/<str:slug>/", render_page, name="render-page"),
    path("game/wizard/", wizard, name="wizard-game"),
    path("language/", set_language, name="set-language"),
    path("random/", get_random_quiz, name="random-quiz"),
    path("", HomeView.as_view(), name="home"),
]
