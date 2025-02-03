from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if obj.writer == request.user:
            return True
        raise PermissionDenied('Not Authorized to do perform this operation.')
