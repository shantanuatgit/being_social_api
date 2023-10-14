from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow user to edit their own post"""

    def has_object_permission(self, request, view, obj):
        """Check user trying to edit their own post"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user
    


class IsLikeOwnerOrReadOnly(permissions.BasePermission):
    """Allow user to delete their own like"""

    def has_object_permission(self, request, view, obj):
        """Check user trying to delete their own like"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.liked_by == request.user



class IsCommentOwnerOrPostOwner(permissions.BasePermission):
    """Allow owners of comment, reply or post to delete them"""

    def has_object_permission(self, request, view, obj):
        print("Checking permissions for user:", request.user)
        print("Comment owner:", obj.commenter)
        print("Post owner:", obj.post.user)
        return request.user == obj.commenter or obj.post.user == request.user