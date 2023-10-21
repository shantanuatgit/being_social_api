from rest_framework import viewsets, generics
from rest_framework.validators import ValidationError
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.db.models import F
from django.db import transaction

from profiles_api import models, serializers, pagination
from .permissions import *


class UserProfileViewSet(viewsets.ModelViewSet):
    """creating and updating profiles Admin use only """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]
    pagination_class = pagination.ProfilePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('full_name', 'email')



class UserCreateApiView(generics.CreateAPIView):
    """Register new user"""
    serializer_class = serializers.UserProfileSerializer



class UserProfileFullUpdate(generics.RetrieveUpdateDestroyAPIView):
    """Retriving user profile or updating full profile"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = [UpdateOwnProfile]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        return models.UserProfile.objects.filter(id=user_id)

    def get_serializer(self, *args, **kwargs):
        """Switch to Restricted mode to hide post for unautheticated user"""
        if self.request.user.is_authenticated:
            return serializers.UserProfileFullSerilizer(*args, **kwargs)
        else:
            return serializers.UserProfileRestrictedSerilizer(*args, **kwargs)

    

    def perform_update(self, serializer):
        user_id = self.kwargs.get('pk')
        try:
            instance = models.UserProfile.objects.get(id=user_id)
        except models.UserProfile.DoesNotExist:
            raise ValidationError("User profile not found")

        new_avatar = serializer.validated_data.get('avatar')
        if new_avatar and instance.avatar:
            instance.avatar.delete(save=False)
                
        serializer.save()

    

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class FollowerFollowingCreateDestroyApiView(generics.CreateAPIView, generics.DestroyAPIView):
    """Handles follow and unfollow the leader """
    serializer_class = serializers.FollowerFollowingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return models.FollowerFollowing.objects.filter(follower=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        leader_id = self.kwargs.get('pk')
        try:
            leader = models.UserProfile.objects.select_for_update().get(pk=leader_id)
        except:
            raise ValidationError("user profile does not exists")
        
        try:
            serializer.save(follower=self.request.user, leader=leader)
            # increment the following atomically by 1 for logged in user
            models.UserProfile.objects.filter(email=self.request.user).update(following_count=F('following_count')+1)
            
            # increment the follower count of leader atomically by 1  
            models.UserProfile.objects.filter(email=leader).update(follower_count=F('follower_count')+1)
        except: raise ValidationError("you are already following this user")

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        leader_id = self.kwargs.get('pk')
        print("this")
        try:
            print(leader_id)
            leader = models.UserProfile.objects.select_for_update().get(pk=leader_id)

            is_following = models.FollowerFollowing.objects.get(
                follower = self.request.user,
                leader = leader
            )

            is_following.delete()
            # decrease the following atomically by 1 for logged in user
            models.UserProfile.objects.filter(email=self.request.user).update(following_count=F('following_count')-1)
            
            # decrease the follower count of leader atomically by 1  
            models.UserProfile.objects.filter(email=leader).update(follower_count=F('follower_count')-1)
            return Response({"detail": "You unfollowed the user successfully"}, status=status.HTTP_204_NO_CONTENT)
        except models.FollowerFollowing.DoesNotExist:
            raise ValidationError("You are not following this user, or this user does not exists.")



class FollowerDestroyApiView(generics.DestroyAPIView, generics.GenericAPIView):
    """Handles removing the follower from followers list"""
    serializer_class = serializers.FollowerFollowingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return models.FollowerFollowing.objects.filter(leader=self.request.user)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        follower_id = self.kwargs.get('pk')
        try:
            follower = models.UserProfile.objects.select_for_update().get(pk=follower_id)

            is_follower = models.FollowerFollowing.objects.get(
                follower = follower,
                leader = self.request.user
            )

            is_follower.delete()
            # decrease the following atomically by 1 for logged in user
            models.UserProfile.objects.filter(email=self.request.user).update(follower_count=F('follower_count')-1)
            
            # decrease the follower count of leader atomically by 1  
            models.UserProfile.objects.filter(email=follower).update(following_count=F('following_count')-1)
            return Response({"detail": "Follower Successfully removed"}, status=status.HTTP_204_NO_CONTENT)
        except models.FollowerFollowing.DoesNotExist:
            raise ValidationError("Follower not found in followers list, or this user does not exists.")




class FollowerListApiView(generics.ListAPIView):
    serializer_class = serializers.FollowerFollowingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    pagination_class = pagination.ProfilePagination

    def get_queryset(self):
        user_email = self.kwargs.get('email')
        return models.FollowerFollowing.objects.filter(leader__email=user_email)
    


class FollowingListApiView(generics.ListAPIView):
    serializer_class = serializers.FollowerFollowingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    pagination_class = pagination.ProfilePagination

    def get_queryset(self):
        user_email = self.kwargs.get('email')
        return models.FollowerFollowing.objects.filter(follower__email=user_email)