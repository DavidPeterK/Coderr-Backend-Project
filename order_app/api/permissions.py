from rest_framework import permissions


class IsCustomerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer_user == request.user or request.user.is_staff
