"""Custom permission classes for boards, tasks, and comments."""

from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """Allow access only to authenticated board owners or board members."""

    message = (
        "Du musst Eigentümer oder Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        """Allow requests only from authenticated users."""
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Allow access when the user owns the board or belongs to it."""
        return (
            obj.owner == request.user
            or obj.members.filter(id=request.user.id).exists()
        )


class IsMember(BasePermission):
    """Allow access only to authenticated members of a board."""

    message = (
        "Du musst Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        """Allow requests only from authenticated users."""
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Allow access when the user belongs to the board."""
        return (
            obj.members.filter(id=request.user.id).exists()
        )


class IsMemberForTask(BasePermission):
    """Allow access only to members of the board that owns a task."""

    message = (
        "Du musst Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        """Allow requests only from authenticated users."""
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Allow access when the user belongs to the task's board."""
        return (
            obj.board.members.filter(id=request.user.id).exists()
        )


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allow task deletion only for the task creator or board owner."""

    message = (
        "Du musst Ersteller der Task oder Eigentümer des Boards sein."
    )

    def has_permission(self, request, view):
        """Allow requests only from authenticated users."""
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Allow access when the user created the task or owns its board."""
        return (
            obj.creator == request.user
            or obj.board.owner == request.user
        )


class IsBoardMemberOfTask(BasePermission):
    """Allow access only to members of the board that owns a task."""

    message = (
        "Du musst Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        """Allow requests only from authenticated users."""
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Allow access when the user belongs to the task's board."""
        return (
            obj.board.members.filter(id=request.user.id).exists()
        )


class IsCommentCreator(BasePermission):
    """Allow requests only from authenticated users for comment operations."""

    def has_permission(self, request, view):
        """Allow requests only from authenticated users."""
        return bool(
            request.user
            and request.user.is_authenticated
        )