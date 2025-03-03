from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Class, Subject, TestCategory, Test, Question, Answer, TestResult
from .serializers import (
    ClassSerializer, SubjectSerializer, TestCategorySerializer, 
    TestSerializer, QuestionSerializer, AnswerSerializer, TestResultSerializer
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
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def start_test(self, request, pk=None):
        """
        Testni boshlash uchun endpoint.
        """
        test = self.get_object()
        questions = test.questions.all()
        
        # Testdagi barcha savollar va ularning javoblari ro‘yxatini qaytarish
        question_data = []
        for question in questions:
            answers = question.answers.all()
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
            'questions': question_data
        })


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Test natijalarini yaratish.
        """
        user = self.request.user
        test_id = self.request.data.get('test')
        test = get_object_or_404(Test, id=test_id)
        answers_data = self.request.data.get('answers', [])

        # Test natijalarini hisoblash
        score = 0
        total_questions = test.questions.count()

        for answer_id in answers_data:
            answer = get_object_or_404(Answer, id=answer_id)
            if answer.is_correct:
                score += 1

        # Test foiz hisobida baholanadi
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0

        serializer.save(user=user, test=test, score=percentage)

    @action(detail=True, methods=['get'])
    def view_result(self, request, pk=None):
        """
        Foydalanuvchi test natijalarini ko‘rish uchun endpoint.
        """
        result = self.get_object()
        return Response({
            'user': result.user.username,
            'test': result.test.name,
            'score': result.score,
            'completed_at': result.completed_at
        })
