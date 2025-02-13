from django.db import models

class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    time_limit = models.IntegerField(help_text="Time in minutes")
    created_by = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="created_tests")
    
    def __str__(self):
        return self.name

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=1024)
    question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Multiple Choice'), ('text_answer', 'Text Answer')])

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=1024)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class TestResult(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.test} - {self.score}'
