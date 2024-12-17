
from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_quiz, name='start_quiz'),
    path('question/<str:session_id>/', views.get_random_question, name='get_random_question'),
    path('submit/<str:session_id>/', views.submit_answer, name='submit_answer'),
    path('summary/<str:session_id>/', views.get_session_summary, name='get_session_summary'),
    
]
            