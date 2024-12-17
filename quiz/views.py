
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json
from .models import Question, UserSession
import uuid

def start_quiz(request):
    session_id = uuid.uuid4().hex
    UserSession.objects.create(session_id=session_id)
    return JsonResponse({'message': 'Quiz session started', 'session_id': session_id})


def get_random_question(request, session_id):
    try:
        session = UserSession.objects.get(session_id=session_id)
        question = random.choice(Question.objects.all())
        return JsonResponse({
            'question_id': question.id,
            'text': question.text,
            'options': {
                'A': question.option_a,
                'B': question.option_b,
                'C': question.option_c,
                'D': question.option_d,
            }
        })
    except UserSession.DoesNotExist:
        return JsonResponse({'error': 'Invalid session ID'}, status=400)
    except IndexError:
        return JsonResponse({'error': 'No questions available'}, status=404)


@csrf_exempt
def submit_answer(request, session_id):
    if request.method == 'POST':
        try:
            session = UserSession.objects.get(session_id=session_id)
            data = json.loads(request.body)
            question_id = data.get('question_id')
            selected_option = data.get('selected_option')

            question = Question.objects.get(id=question_id)
            session.total_questions += 1
            if question.correct_option == selected_option:
                session.correct_answers += 1
            else:
                session.incorrect_answers += 1
            session.save()
            return JsonResponse({
                'message': 'Answer submitted',
                'is_correct': question.correct_option == selected_option,
            })
        except UserSession.DoesNotExist:
            return JsonResponse({'error': 'Invalid session ID'}, status=400)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Invalid question ID'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_session_summary(request, session_id):
    try:
        session = UserSession.objects.get(session_id=session_id)
        return JsonResponse({
            'total_questions': session.total_questions,
            'correct_answers': session.correct_answers,
            'incorrect_answers': session.incorrect_answers,
        })
    except UserSession.DoesNotExist:
        return JsonResponse({'error': 'Invalid session ID'}, status=400)
            