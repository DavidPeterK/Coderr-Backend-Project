from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow:
    - Any authenticated user to retrieve profiles.
    - Only the owner or an admin to update a profile.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        return request.user.is_staff or obj.user == request.user
