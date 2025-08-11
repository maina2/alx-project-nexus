from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.roles == 'admin'

class IsAdminOrCreator(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow deletion if user is admin or the poll's creator
        return request.user.roles == 'admin' or obj.creator == request.user

class IsPollCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow action only if the user is the poll's creator
        return request.user and request.user.is_authenticated and obj.creator == request.user