# users/permissions.py
from rest_framework import permissions

class IsFinanceUser(permissions.BasePermission):
    """
    Allows access only to users with the 'finance' role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'finance')

class IsAdmissionUser(permissions.BasePermission):
    """
    Allows access only to users with 'admission' or 'admin' roles.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['admission', 'admin'])
