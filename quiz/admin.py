from django.contrib import admin
from quiz.models import Map, Quiz, QuizComment, Question

class MapAdmin(admin.ModelAdmin):
    list_display = ("name", "license")

class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "author")

admin.site.register(Map, MapAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizComment)
admin.site.register(Question)