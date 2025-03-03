from django.contrib import admin
from .models import Class, Subject, TestCategory, Test, Question, Answer, TestResult


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_obj')
    list_filter = ('class_obj',)


@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    list_filter = ('subject',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'time_limit', 'created_by')
    list_filter = ('category', 'created_by')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'test', 'question_type')
    list_filter = ('test', 'question_type')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test', 'score', 'completed_at')
    list_filter = ('user', 'test')
