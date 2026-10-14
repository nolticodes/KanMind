from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    message = (
        "Du musst Eigentümer oder Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user
            or obj.members.filter(id=request.user.id).exists()
        )


class IsMember(BasePermission):
    message = (
        "Du musst Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.members.filter(id=request.user.id).exists()
        )


class IsMemberForTask(BasePermission):
    message = (
        "Du musst Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.board.members.filter(id=request.user.id).exists()
        )


class IsTaskCreatorOrBoardOwner(BasePermission):
    message = (
        "Du musst Ersteller der Task oder Eigentümer des Boards sein."
    )

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.creator == request.user
            or obj.board.owner == request.user
        )


class IsBoardMemberOfTask(BasePermission):
    message = (
        "Du musst Mitglied dieses Boards sein."
    )

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.board.members.filter(id=request.user.id).exists()
        )

class IsCommentCreator(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
        )