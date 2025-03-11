from django.contrib import admin
from .models import Class, Subject, TestCategory, Test, Question, Answer, TestResult


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_obj')
    list_filter = ('class_obj',)
    search_fields = ('name', 'class_obj__name')
    ordering = ('id',)


@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    list_filter = ('subject',)
    search_fields = ('name', 'subject__name')
    ordering = ('id',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'time_limit', 'created_by')
    list_filter = ('category', 'created_by')
    search_fields = ('name', 'category__name', 'created_by__username')
    ordering = ('-id',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'test', 'question_type')
    list_filter = ('test', 'question_type')
    search_fields = ('text', 'test__name')
    ordering = ('id',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('text', 'question__text')
    ordering = ('id',)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test', 'score', 'completed_at')
    list_filter = ('user', 'test')
    search_fields = ('user__username', 'test__name')
    ordering = ('-completed_at',)
    readonly_fields = ('completed_at',)
