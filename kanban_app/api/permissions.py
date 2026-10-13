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