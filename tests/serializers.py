from rest_framework import serializers
from .models import Class, Subject, TestCategory, Test, Question, Answer, TestResult


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class_obj = ClassSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'


class TestCategorySerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = TestCategory
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    category = TestCategorySerializer(read_only=True)

    class Meta:
        model = Test
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    test = TestSerializer(read_only=True)

    class Meta:
        model = TestResult
        fields = '__all__'
