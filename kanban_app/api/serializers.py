from rest_framework import serializers

from kanban_app.models import Board, Task, Comment
from auth_app.models import User


class GetBoardsListSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Board
        fields = ['title', 'members']


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "fullname",
        ]


class BoardTaskInfoSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Board
        fields = [
            'title',
            'members'
        ]


class PostTaskInBoardRequestSerializer(serializers.ModelSerializer):
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
        return 0


class PatchTaskInBoardRequestSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = Comment
        fields = [
            'content'
        ]


class GetTasksAssignedToMeSerializer(serializers.ModelSerializer):

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

