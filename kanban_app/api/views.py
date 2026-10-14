from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model          # später entfernen
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from kanban_app.models import Board, Task, Comment
from auth_app.models import User

from .permissions import IsBoardOwnerOrMember, IsMember, IsMemberForTask, IsTaskCreatorOrBoardOwner, IsBoardMemberOfTask

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
    GetCommentsListSerializer,
    PostCommentsInListSerializer,
    GetTasksAssignedToMeSerializer
)


class BoardView(generics.ListCreateAPIView):

    queryset = Board.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardOwnerOrMember]

    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user)
            | Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetBoardsListSerializer
        if self.request.method == "POST":
            return CreateBoardSerializer
        return GetBoardsListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardOwnerOrMember]

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

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsMember]

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsMemberForTask]
    queryset = Task.objects.all()
    serializer_class = PatchTaskInBoardRequestSerializer

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsMemberForTask()]
        if self.request.method == "DELETE":
            return [IsTaskCreatorOrBoardOwner()]

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


class CommentsListView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardMemberOfTask]
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCommentsInListSerializer

        return GetCommentsListSerializer

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, task)

        comments = task.comments.all().order_by("created_at")
        serializer = GetCommentsListSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, task)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = serializer.save(
            task=task,
            author=request.user
        )

        response_serializer = GetCommentsListSerializer(comment)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class CommentIDView(generics.DestroyAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardMemberOfTask]
    queryset = Comment.objects.all()
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(
            task_id=self.kwargs["task_id"]
        )


class AssigneeView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetTasksAssignedToMeSerializer

    def get_queryset (self): 
        return Task.objects.filter(assignee = self.request.user)

class ReviewerView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetTasksAssignedToMeSerializer

    def get_queryset (self): 
        return Task.objects.filter(reviewer = self.request.user)