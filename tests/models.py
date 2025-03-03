from django.db import models
from users.models import User


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


class TestResult(models.Model):
    """Test natijalari"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.test} - {self.score}'
