from django.db import models
from users.models import User
import random


class Class(models.Model):
    """Sinf modeli"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Fan modeli"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.class_obj} - {self.name}"


class TestCategory(models.Model):
    """Test turi (kategoriya)"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="test_categories")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject} - {self.name}"


class Test(models.Model):
    """Test modeli"""
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name="tests")
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.IntegerField(help_text="Time in minutes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tests")

    def __str__(self):
        return self.name


class Question(models.Model):
    """Savollar modeli"""
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=1024)
    question_type = models.CharField(
        max_length=50,
        choices=[
            ('multiple_choice', 'Multiple Choice'),
            ('text_answer', 'Text Answer')
        ]
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Javoblar modeli"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=1024)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserTestSession(models.Model):
    """Foydalanuvchi uchun test sessiyasi (Random savollar tarib qilinadi)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def generate_random_questions(self):
        """Har bir foydalanuvchi uchun savollar tasodifiy tartibda beriladi"""
        all_questions = list(self.test.questions.all())
        random.shuffle(all_questions)
        self.questions.set(all_questions)

    def __str__(self):
        return f"{self.user} - {self.test} (Session)"


class TestResult(models.Model):
    """Test natijalari"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.test} - {self.score}'


class UserAnswer(models.Model):
    """Foydalanuvchi javoblari"""
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name="user_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.test_result.user} - {self.question} - {'Correct' if self.is_correct else 'Wrong'}"
