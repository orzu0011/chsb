from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClassViewSet, SubjectViewSet, TestCategoryViewSet, 
    TestViewSet, QuestionViewSet, AnswerViewSet, TestResultViewSet
)

router = DefaultRouter()
router.register(r'classes', ClassViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'test-categories', TestCategoryViewSet)
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'test-results', TestResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
