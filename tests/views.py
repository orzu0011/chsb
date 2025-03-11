from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
import random
from .models import Class, Subject, TestCategory, Test, Question, Answer, TestResult, UserAnswer
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
        test = self.get_object()
        questions = list(test.questions.all())
        random.shuffle(questions)
        
        question_data = []
        for question in questions:
            answers = list(question.answers.all())
            random.shuffle(answers)
            answer_data = [{'id': ans.id, 'text': ans.text} for ans in answers]
            question_data.append({
                'id': question.id,
                'text': question.text,
                'question_type': question.question_type,
                'answers': answer_data
            })
        
        start_time = datetime.now().isoformat()
        
        return Response({
            'message': 'Test started successfully',
            'test_id': test.id,
            'test_name': test.name,
            'time_limit': test.time_limit,
            'start_time': start_time,
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

        score = 0
        total_questions = test.questions.count()
        incorrect_answers = []
        user_answers_bulk = []
        answers_by_question = {q.id: [] for q in test.questions.all()}

        for answer_id in answers_data:
            answer = get_object_or_404(Answer, id=answer_id)
            answers_by_question[answer.question.id].append(answer)

        for question in test.questions.all():
            user_answers = answers_by_question.get(question.id, [])
            correct_answers = list(question.answers.filter(is_correct=True))

            is_correct = False
            if question.question_type == 'single_choice':
                is_correct = len(user_answers) == 1 and user_answers[0] in correct_answers
            elif question.question_type == 'multiple_choice':
                is_correct = set(user_answers) == set(correct_answers)

            if is_correct:
                score += 1
            else:
                incorrect_answers.append({
                    'question': question.text,
                    'your_answer': [ans.text for ans in user_answers],
                    'correct_answer': [ans.text for ans in correct_answers]
                })

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        test_result = serializer.save(user=user, test=test, score=percentage)

        for question in test.questions.all():
            user_answers = answers_by_question.get(question.id, [])
            for answer in user_answers:
                user_answers_bulk.append(UserAnswer(
                    test_result=test_result,
                    question=question,
                    selected_answer=answer,
                    is_correct=answer.is_correct
                ))

        UserAnswer.objects.bulk_create(user_answers_bulk)

        return Response({
            'message': 'Test completed successfully',
            'test_id': test.id,
            'score': percentage,
            'incorrect_answers': incorrect_answers
        })

    @action(detail=True, methods=['get'])
    def view_result(self, request, pk=None):
        result = self.get_object()
        incorrect_answers = []

        for question in result.test.questions.all():
            user_answers = Answer.objects.filter(question=question, is_correct=False)
            correct_answers = [ans.text for ans in question.answers.filter(is_correct=True)]

            if user_answers.exists():
                incorrect_answers.append({
                    'question': question.text,
                    'your_answer': [ans.text for ans in user_answers],
                    'correct_answer': correct_answers
                })

        return Response({
            'user': result.user.username,
            'test': result.test.name,
            'score': result.score,
            'completed_at': result.completed_at,
            'incorrect_answers': incorrect_answers
        })
