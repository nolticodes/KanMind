"""Serializers for boards, tasks, comments, and user summary data."""

from rest_framework import serializers

from kanban_app.models import Board, Task, Comment
from auth_app.models import User


class GetBoardsListSerializer(serializers.ModelSerializer):
    """Serialize boards with annotated member and task count values."""

    member_count = serializers.IntegerField(read_only = True)
    ticket_count = serializers.IntegerField(read_only = True)
    tasks_to_do_count = serializers.IntegerField(read_only = True)
    tasks_high_prio_count = serializers.IntegerField(read_only = True)

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id'
        ]


class CreateBoardSerializer(serializers.ModelSerializer):
    """Validate data required to create a new board."""

    class Meta:
        model = Board
        fields = ['title', 'members']


class UserSummarySerializer(serializers.ModelSerializer):
    """Serialize essential public information about a user."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "fullname",
        ]


class BoardTaskInfoSerializer(serializers.ModelSerializer):
    """Serialize task information displayed within a board detail response."""

    assignee = UserSummarySerializer(read_only=True)
    reviewer = UserSummarySerializer(read_only=True)

    comments_count = serializers.IntegerField(read_only = True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        ]


class GetBoardDetailSerializer(serializers.ModelSerializer):
    """Serialize a board with its members and related tasks."""

    members = UserSummarySerializer(
        many=True,
        read_only=True
    )

    tasks = BoardTaskInfoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_id',
            'members',
            'tasks',
        ]


class PatchBoardDetailResponseSerializer(serializers.ModelSerializer):
    """Serialize updated board data after a partial update."""

    owner_data = UserSummarySerializer(
        source="owner",
        read_only=True
    )

    members_data = UserSummarySerializer(
        source="members",
        many=True,
        read_only=True
    )

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_data',
            'members_data'
        ]


class PatchBoardDetailRequestSerializer(serializers.ModelSerializer):
    """Validate fields that can be partially updated on a board."""

    class Meta:
        model = Board
        fields = [
            'title',
            'members'
        ]


class PostTaskInBoardRequestSerializer(serializers.ModelSerializer):
    """Validate data required to create a task within a board."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee",
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date'
        ]


class PostTaskInBoardResponseSerializer(serializers.ModelSerializer):
    """Serialize a newly created task with related user information."""

    assignee = UserSummarySerializer(
        read_only=True
    )

    reviewer = UserSummarySerializer(
        read_only=True
    )

    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count'
        ]

    def get_comments_count(self, obj):
        """Return the initial comment count for a newly created task."""
        return 0


class PatchTaskInBoardRequestSerializer(serializers.ModelSerializer):
    """Validate fields that can be partially updated on a task."""

    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee",
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'assignee_id',
            'reviewer_id',
            'due_date'
        ]


class PatchTaskInBoardResponseSerializer(serializers.ModelSerializer):
    """Serialize task data after a partial update."""

    assignee = UserSummarySerializer(
        read_only=True
    )

    reviewer = UserSummarySerializer(
        read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date'
        ]


class GetCommentsListSerializer(serializers.ModelSerializer):
    """Serialize comments with the author's full name."""

    author = serializers.CharField(
        source="author.fullname",
        read_only=True
    )

    class Meta: 
        model = Comment
        fields = [
            'id',
            'created_at',
            'author',
            'content'
        ]


class PostCommentsInListSerializer(serializers.ModelSerializer):
    """Validate content for creating a new task comment."""

    class Meta:
        model = Comment
        fields = [
            'content'
        ]


class GetTasksAssignedToMeSerializer(serializers.ModelSerializer):
    """Serialize tasks assigned to or reviewed by the authenticated user."""

    assignee = UserSummarySerializer(
        read_only=True
    )
    
    reviewer = UserSummarySerializer(
        read_only=True
    )

    comments_count = serializers.IntegerField(read_only = True)

    class Meta:
        model = Task
        fields = [
            'id',
            'board',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'reviewer',
            'due_date',
            'comments_count'
        ]