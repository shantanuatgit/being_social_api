from rest_framework import serializers
from profiles_api import models
from pic_board.serializers import PicPostSerializer



class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'full_name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'} 
            }
        }
    def create(self, validated_data):
        """Create and return new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            full_name = validated_data['full_name'],
            password = validated_data['password'],
            
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)



class UserProfileRestrictedSerilizer(serializers.ModelSerializer):
    """View only serilizer for non registered and unauthenticated  users"""
    class Meta:
        model = models.UserProfile
        fields = ['email', 'full_name', 'avatar', 'bio', 'post_count', 'follower_count', 'following_count', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'following_count': {'read_only': True},
            'follower_count': {'read_only': True},
            'post_count': {'read_only': True}
        }




class UserProfileFullSerilizer(serializers.ModelSerializer):
    """Fill or update other fields of user profile after registration"""
    pic_post = PicPostSerializer(many=True, read_only=True, source='picpost_set')

    class Meta:
        model = models.UserProfile
        fields = ['email', 'full_name', 'avatar', 'bio', 'post_count', 'follower_count', 'following_count', 'created_at', 'updated_at', 'pic_post']
        extra_kwargs = {
            'updated_at': {'read_only': True},
            'created_at': {'read_only': True},
            'following_count': {'read_only': True},
            'follower_count': {'read_only': True},
            'post_count': {'read_only': True}
        }



class FollowerFollowingSerializer(serializers.ModelSerializer):
    """Handle followers and following"""
    leader = serializers.StringRelatedField()
    follower = serializers.StringRelatedField()

    class Meta:
        model = models.FollowerFollowing
        fields = ['leader', 'follower']
        extra_kwargs = {
            'leader': {'read_only': True},
            'follower': {'read_only': True}
        }
