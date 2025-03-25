from rest_framework import serializers
from .models import Class, Subject, TestCategory, Test, Question, Answer, TestResult
from users.models import User
import random

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'answers']

class UserAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer_id = serializers.IntegerField()

class TestDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'name', 'description', 'time_limit', 'questions']

class TestResultSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    test = serializers.StringRelatedField()
    
    class Meta:
        model = TestResult
        fields = '__all__'

class TestResultDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    test = serializers.StringRelatedField()
    incorrect_answers = serializers.SerializerMethodField()
    correct_answers = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['user', 'test', 'score', 'incorrect_answers', 'correct_answers']

    def get_incorrect_answers(self, obj):
        incorrect_answers = Answer.objects.filter(question__test=obj.test, is_correct=False)
        return AnswerSerializer(incorrect_answers, many=True).data

    def get_correct_answers(self, obj):
        correct_answers = Answer.objects.filter(question__test=obj.test, is_correct=True)
        return AnswerSerializer(correct_answers, many=True).data
