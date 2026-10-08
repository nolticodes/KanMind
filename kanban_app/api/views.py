from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth import get_user_model          # später entfernen
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from kanban_app.models import Board, Task
from auth_app.models import User

from .serializers import (
    GetBoardsListSerializer,
    CreateBoardSerializer,
    GetBoardDetailSerializer,
    PatchBoardDetailResponseSerializer,
    PatchBoardDetailRequestSerializer,
    UserSummarySerializer,
    PostTaskInBoardRequestSerializer,
    PostTaskInBoardResponseSerializer,
    PatchTaskInBoardRequestSerializer,
    PatchTaskInBoardResponseSerializer,
)


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


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Board.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetBoardDetailSerializer
        if self.request.method == "PATCH":
            return PatchBoardDetailRequestSerializer

        return GetBoardDetailSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        response_serializer = PatchBoardDetailResponseSerializer(instance)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )


class FindUserWithEmailView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email")

        if not email:
            return Response(
                {"detail": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"detail": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"detail": "Email not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSummarySerializer(user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CreateTaskInBoardView(generics.CreateAPIView):
    serializer_class = PostTaskInBoardRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = PostTaskInBoardResponseSerializer(
            serializer.instance)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Task.objects.all()
    serializer_class = PatchTaskInBoardRequestSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        response_serializer = PatchTaskInBoardResponseSerializer(
            serializer.instance)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )
