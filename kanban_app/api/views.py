"""API views for boards, tasks, comments, and user lookup."""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model          # später entfernen
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Prefetch

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


def boards_with_counts():
    """Return boards annotated with member and task-related counts."""
    return Board.objects.annotate(
        member_count=Count("members", distinct=True),
        ticket_count=Count("tasks", distinct=True),
        tasks_to_do_count=Count(
            "tasks",
            filter=Q(tasks__status="to-do"),
            distinct=True,
        ),
        tasks_high_prio_count=Count(
            "tasks",
            filter=Q(tasks__priority="high"),
            distinct=True,
        ),
    )


def get_comments_counts():
    """Return tasks annotated with the number of related comments."""
    return Task.objects.annotate(
        comments_count=Count("comments", distinct=True)
    )


class BoardView(generics.ListCreateAPIView):
    """List accessible boards and create new boards for authenticated users."""

    queryset = Board.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardOwnerOrMember]

    def get_queryset(self):
        """Return boards where the current user is owner or member."""
        return boards_with_counts().filter(
            Q(owner=self.request.user)
            | Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        """Select the appropriate serializer for GET and POST requests."""
        if self.request.method == "GET":
            return GetBoardsListSerializer
        if self.request.method == "POST":
            return CreateBoardSerializer
        return GetBoardsListSerializer

    def perform_create(self, serializer):
        """Create a board and assign the current user as its owner."""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a board and return it with annotated count values."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        board = boards_with_counts().get(pk=serializer.instance.pk)

        response_serializer = GetBoardsListSerializer(board)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, partially update, or delete a single board."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardOwnerOrMember]

    def get_queryset(self):
        """Return boards with tasks preloaded and annotated with comment counts."""
        return Board.objects.prefetch_related(
            Prefetch(
                "tasks",
                queryset=get_comments_counts()
            )
        )

    def get_serializer_class(self):
        """Select the appropriate serializer for GET and PATCH requests."""
        if self.request.method == "GET":
            return GetBoardDetailSerializer

        if self.request.method == "PATCH":
            return PatchBoardDetailRequestSerializer

        return GetBoardDetailSerializer

    def partial_update(self, request, *args, **kwargs):
        """Partially update a board and return the updated board data."""
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
    """Find a user by a validated email address."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Validate an email query parameter and return matching user data."""
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
    """Create a new task within a board."""

    serializer_class = PostTaskInBoardRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsMember]

    def create(self, request, *args, **kwargs):
        """Validate, create, and return a newly created task."""
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
    """Partially update or delete a single task."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsMemberForTask]
    queryset = Task.objects.all()
    serializer_class = PatchTaskInBoardRequestSerializer

    def get_permissions(self):
        """Apply permissions based on the current request method."""
        if self.request.method == "PATCH":
            return [IsMemberForTask()]
        if self.request.method == "DELETE":
            return [IsTaskCreatorOrBoardOwner()]

    def partial_update(self, request, *args, **kwargs):
        """Partially update a task and return its updated data."""
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
    """List comments for a task or create a new comment."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardMemberOfTask]
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        """Select the request serializer for POST and response serializer otherwise."""
        if self.request.method == "POST":
            return PostCommentsInListSerializer

        return GetCommentsListSerializer

    def get(self, request, *args, **kwargs):
        """Return all comments for the task identified in the URL."""
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
        """Create a comment for the task identified in the URL."""
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
    """Delete a comment belonging to a specific task."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsBoardMemberOfTask]
    queryset = Comment.objects.all()
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        """Return comments limited to the task identified in the URL."""
        return Comment.objects.filter(
            task_id=self.kwargs["task_id"]
        )


class AssigneeView(generics.ListAPIView):
    """List tasks assigned to the authenticated user."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetTasksAssignedToMeSerializer

    def get_queryset(self):
        """Return tasks assigned to the current user with comment counts."""
        return get_comments_counts().filter(
            assignee=self.request.user
        )


class ReviewerView(generics.ListAPIView):
    """List tasks where the authenticated user is assigned as reviewer."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GetTasksAssignedToMeSerializer

    def get_queryset(self):
        """Return tasks reviewed by the current user with comment counts."""
        return get_comments_counts().filter(
            reviewer=self.request.user
        )