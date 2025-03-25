from rest_framework import serializers
from .models import (
    Class, Subject, TestCategory, Test, Question, Answer,
    UserTestSession, TestResult, UserAnswer
)


class ClassSerializer(serializers.ModelSerializer):
    """Sinf serializer"""
    class Meta:
        model = Class
        fields = ['id', 'name']


class SubjectSerializer(serializers.ModelSerializer):
    """Fan serializer"""
    class_obj = ClassSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'class_obj', 'name']


class TestCategorySerializer(serializers.ModelSerializer):
    """Test kategoriyasi serializer"""
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = TestCategory
        fields = ['id', 'subject', 'name']


class AnswerSerializer(serializers.ModelSerializer):
    """Javob serializer"""
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    """Savol serializer"""
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'test', 'text', 'question_type', 'answers']


class TestSerializer(serializers.ModelSerializer):
    """Test serializer (Savollar bilan birga keladi)"""
    category = TestCategorySerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)  # Test ichida savollar keladi

    class Meta:
        model = Test
        fields = ['id', 'category', 'name', 'description', 'time_limit', 'created_by', 'questions']


class UserTestSessionSerializer(serializers.ModelSerializer):
    """Foydalanuvchi test sessiyasi serializer"""
    user = serializers.StringRelatedField(read_only=True)
    test = TestSerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = UserTestSession
        fields = ['id', 'user', 'test', 'questions', 'started_at', 'completed_at']


class TestResultSerializer(serializers.ModelSerializer):
    """Test natijalari serializer"""
    user = serializers.StringRelatedField(read_only=True)
    test = TestSerializer(read_only=True)

    class Meta:
        model = TestResult
        fields = ['id', 'user', 'test', 'score', 'completed_at']


class UserAnswerSerializer(serializers.ModelSerializer):
    """Foydalanuvchi javoblari serializer"""
    test_result = TestResultSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    selected_answer = AnswerSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['id', 'test_result', 'question', 'selected_answer', 'is_correct']
