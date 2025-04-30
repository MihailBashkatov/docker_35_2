from rest_framework import permissions


class ModeratorAccessPermission(permissions.BasePermission):
    """
    Check if user is in Group Moderators
    """

    message = "Adding permissions for moderators."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True
        return False
