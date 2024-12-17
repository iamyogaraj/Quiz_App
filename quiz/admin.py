
from django.contrib import admin
from .models import Question, UserSession

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'correct_option')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'total_questions', 'correct_answers', 'incorrect_answers')
            