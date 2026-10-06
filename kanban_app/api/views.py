from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from kanban_app.models import Board

from .serializers import GetBoardsListSerializer

class BoardView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = GetBoardsListSerializer
    permission_classes = [AllowAny]