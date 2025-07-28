from rest_framework.permissions import BasePermission

class IsAPIUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='api_users').exists()