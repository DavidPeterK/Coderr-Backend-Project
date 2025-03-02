from rest_framework import permissions


class IsReviewerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user or request.user.is_staff
