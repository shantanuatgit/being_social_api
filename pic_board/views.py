from django.db.models import F, Q
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import ValidationError

from pic_board import serializers, models
from profiles_api.models import UserProfile, FollowerFollowing
from profiles_api import pagination

from .permissions import IsOwnerOrReadOnly, IsCommentOwnerOrPostOwner, IsLikeOwnerOrReadOnly
# Create your views here.



class PicPostCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.PicPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        UserProfile.objects.filter(email=self.request.user).update(post_count=F('post_count')+1)



class PicPostRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PicPost.objects.all()
    serializer_class = serializers.PicPostSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = pagination.ProfilePagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_serializer(self, *args, **kwargs):
        """Restrict update on image"""
        serializer = super().get_serializer(*args, **kwargs)

        if self.request.method in ('PUT', 'PATCH'):
            serializer.fields['image'].read_only=True
        return serializer

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.delete()
        UserProfile.objects.filter(email=self.request.user).update(post_count=F('post_count')-1)



class LikePostCreateListApiView(generics.ListCreateAPIView):
    serializer_class = serializers.LikePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """List the users who have liked the selected post"""
        post_id = self.kwargs.get('pk')
        return models.LikePost.objects.filter(post__pk=post_id).select_related('liked_by')
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = (IsOwnerOrReadOnly,)
        return super().get_permissions()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        user = self.request.user

        try:
            post = models.PicPost.objects.select_for_update().get(pk=post_id)
            like_post = models.LikePost(post=post, liked_by=user)
            like_post.save()

            models.PicPost.objects.filter(pk=post_id).update(likes_count=F('likes_count')+1)
        except:
            raise ValidationError("user have already liked the post.")

        return Response({"detail": "Post Liked successfully."}, status=status.HTTP_201_CREATED)



class LikePostDestroyApiView(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.LikePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """List the user who have liked the selected post"""
        like_id = self.kwargs.get('pk')
        return models.LikePost.objects.filter(pk=like_id)
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = (IsLikeOwnerOrReadOnly,)
        return super().get_permissions()
    
    @transaction.atomic
    def perform_destroy(self, instance):
        try:
            post_id = instance.post.id
            instance.delete()
            models.PicPost.objects.filter(pk=post_id).update(likes_count=F('likes_count')-1)
        except:
            raise ValidationError("something went wrong, please try again later.")
        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)




class CommentPostApiView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentPostSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = pagination.ProfilePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return models.CommentPost.objects.filter(post__pk=post_id, reply_to_comment__isnull=True).select_related('reply_to_comment')

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        parent_comment_id = self.kwargs.get('parent_comment_id')
        user = self.request.user
        content = request.data.get('content')

        try:
            post = models.PicPost.objects.select_for_update().get(pk=post_id)

            if parent_comment_id is not None:
                reply_to_comment = models.CommentPost.objects.select_for_update().get(pk=parent_comment_id)
                comment_post = models.CommentPost(post=post, commenter=user, content=content, reply_to_comment=reply_to_comment)
            else:
                comment_post = models.CommentPost(post=post, commenter=user, content=content)
            
            comment_post.save()
            models.PicPost.objects.filter(pk=post_id).update(comments_count=F('comments_count')+1)
        except models.PicPost.DoesNotExist:
            raise ValidationError("Post does not exist.")
        except models.CommentPost.DoesNotExist:
            raise ValidationError("Parent comment does not exist.")

        return Response({"detail": "Comment added successfully."}, status=status.HTTP_201_CREATED)



class CommentPostDestroyApiView(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.CommentPostSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = pagination.ProfilePagination
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = (IsCommentOwnerOrPostOwner,)
        return super().get_permissions()

    def get_queryset(self):
        comment_id = self.kwargs.get('pk')
        return models.CommentPost.objects.filter(pk=comment_id)
    
    @transaction.atomic
    def perform_destroy(self, instance):
        try: 
            post_id = instance.post.id
            instance.delete()
            models.PicPost.objects.filter(pk=post_id).update(comments_count=F('comments_count')-1)
        except models.PicPost.DoesNotExist:
            raise ValidationError("This post does not exists")
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class PostFeedListApiView(generics.ListAPIView):
    serializer_class = serializers.PicPostSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = pagination.ProfilePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pic_posts = models.PicPost.objects.filter(Q(user__leader__follower=user)).order_by('-created_at')
        return pic_posts