from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user trying to edit their own profile"""
        print(f"Request User: {request.user}")
        print(f"Object User: {obj}")
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj == request.user
    