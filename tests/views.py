from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Test, Question, TestResult
from .serializers import TestSerializer, TestResultSerializer
from users.models import User

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def start_test(self, request, pk=None):
        test = self.get_object()
        user = request.user

        # You can add logic to initiate a test here
        return Response({'message': 'Test started successfully'})

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        test_id = self.request.data.get('test')
        test = Test.objects.get(id=test_id)

        # Calculate score based on submitted answers (you can adjust as needed)
        score = 0  # Placeholder for score calculation logic
        serializer.save(user=user, score=score, test=test)

    @action(detail=True, methods=['get'])
    def view_result(self, request, pk=None):
        result = self.get_object()
        return Response({'result': result.score})
