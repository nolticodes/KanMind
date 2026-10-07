from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth import get_user_model          # später entfernen

from kanban_app.models import Board

from .serializers import GetBoardsListSerializer, CreateBoardSerializer

class BoardView(generics.ListCreateAPIView):

    queryset = Board.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetBoardsListSerializer
        if self.request.method == "POST":
            return CreateBoardSerializer
    
    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)  -> Später wieder hinzufügen, rest unten entfernen
        User = get_user_model()
        test_user = User.objects.get(email="example@mail.de")
        serializer.save(owner=test_user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = GetBoardsListSerializer(serializer.instance)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )