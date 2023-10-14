from rest_framework import serializers

from pic_board import models

class PicPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = models.PicPost
        fields = '__all__'
        extra_kwargs = {
            'likes_count': {'read_only':True},
            'created_at': {'read_only':True},
            'updated_at': {'read_only':True},
            'comments_count': {'read_only':True},
        }



class LikePostSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    liked_by = serializers.StringRelatedField()

    class Meta:
        model = models.LikePost
        fields = ['post', 'liked_by']



class CommentPostSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()
    commenter = serializers.StringRelatedField()
    reply_to_comment = serializers.SerializerMethodField()

    class Meta:
        model = models.CommentPost
        fields = ['id', 'post', 'commenter', 'content', 'created_at', 'updated_at', 'reply_to_comment']
        extra_kwargs = {
            'created_at': {'read_only':True},
            'updated_at': {'read_only':True},
        }
    def get_reply_to_comment(self, obj):
        # Filter and serialize replies for the current comment
        replies = models.CommentPost.objects.filter(reply_to_comment=obj)
        return CommentPostSerializer(replies, many=True).data
   