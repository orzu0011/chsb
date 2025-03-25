from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
import random
from .models import (
    Class, Subject, TestCategory, Test, Question, Answer, 
    TestResult, UserAnswer, UserTestSession
)
from .serializers import (
    ClassSerializer, SubjectSerializer, TestCategorySerializer, 
    TestSerializer, QuestionSerializer, AnswerSerializer, 
    TestResultSerializer, UserTestSessionSerializer
)


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class TestCategoryViewSet(viewsets.ModelViewSet):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer


class TestViewSet(viewsets.ModelViewSet):
    """Testlarni ko‘rish, yaratish va boshlash"""
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def start_test(self, request, pk=None):
        """Testni boshlash va tasodifiy savollarni qaytarish"""
        test = self.get_object()
        user = request.user

        # Foydalanuvchi uchun test sessiyasi yaratish
        session = UserTestSession.objects.create(user=user, test=test)
        session.generate_random_questions()

        # Savollarni javoblar bilan birga shakllantirish
        question_data = []
        for question in session.questions.all():
            answers = list(question.answers.all())
            random.shuffle(answers)
            answer_data = [{'id': ans.id, 'text': ans.text} for ans in answers]
            question_data.append({
                'id': question.id,
                'text': question.text,
                'question_type': question.question_type,
                'answers': answer_data
            })

        return Response({
            'message': 'Test started successfully',
            'test_id': test.id,
            'test_name': test.name,
            'time_limit': test.time_limit,
            'start_time': datetime.now().isoformat(),
            'questions': question_data
        })


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class TestResultViewSet(viewsets.ModelViewSet):
    """Test natijalari uchun ViewSet"""
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Test natijasini saqlash"""
        user = self.request.user
        test_id = self.request.data.get('test')
        test = get_object_or_404(Test, id=test_id)
        answers_data = self.request.data.get('answers', [])
        start_time = self.request.data.get('start_time')

        if not start_time:
            return Response({'error': 'Start time is required'}, status=400)

        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.now()

        if (end_time - start_time).total_seconds() > test.time_limit * 60:
            return Response({'error': 'Test time expired'}, status=400)

        # Foydalanuvchi javoblarini saqlash
        score = 0
        incorrect_answers = []
        user_answers_bulk = []
        question_map = {q.id: q for q in test.questions.all()}
        answer_map = {a.id: a for a in Answer.objects.filter(question__in=question_map.values())}

        for answer_id in answers_data:
            answer = answer_map.get(answer_id)
            if answer:
                question = question_map[answer.question.id]
                user_answers_bulk.append(UserAnswer(
                    test_result=None,
                    question=question,
                    selected_answer=answer,
                    is_correct=answer.is_correct
                ))

        # To‘g‘ri javoblar sonini hisoblash
        for question in test.questions.all():
            correct_answers = set(question.answers.filter(is_correct=True))
            user_selected = {ua.selected_answer for ua in user_answers_bulk if ua.question == question}

            is_correct = user_selected == correct_answers
            if is_correct:
                score += 1
            else:
                incorrect_answers.append({
                    'question': question.text,
                    'your_answer': [ans.text for ans in user_selected],
                    'correct_answer': [ans.text for ans in correct_answers]
                })

        percentage = (score / test.questions.count()) * 100 if test.questions.count() > 0 else 0
        test_result = serializer.save(user=user, test=test, score=percentage)

        # Test natijasiga user javoblarini bog‘lash
        for ua in user_answers_bulk:
            ua.test_result = test_result

        UserAnswer.objects.bulk_create(user_answers_bulk)

        return Response({
            'message': 'Test completed successfully',
            'test_id': test.id,
            'score': percentage,
            'incorrect_answers': incorrect_answers
        })

    @action(detail=True, methods=['get'])
    def view_result(self, request, pk=None):
        """Test natijalarini ko‘rish"""
        result = self.get_object()
        incorrect_answers = []

        for answer in UserAnswer.objects.filter(test_result=result, is_correct=False):
            correct_answers = [ans.text for ans in answer.question.answers.filter(is_correct=True)]
            incorrect_answers.append({
                'question': answer.question.text,
                'your_answer': answer.selected_answer.text if answer.selected_answer else "No Answer",
                'correct_answer': correct_answers
            })

        return Response({
            'user': result.user.username,
            'test': result.test.name,
            'score': result.score,
            'completed_at': result.completed_at,
            'incorrect_answers': incorrect_answers
        })


class UserTestSessionViewSet(viewsets.ModelViewSet):
    """Foydalanuvchi test sessiyasi"""
    queryset = UserTestSession.objects.all()
    serializer_class = UserTestSessionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def session_questions(self, request, pk=None):
        """Foydalanuvchi sessiyasidagi savollarni olish"""
        session = self.get_object()
        questions = session.questions.all()
        return Response(QuestionSerializer(questions, many=True).data)

