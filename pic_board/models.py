from django.db import models
import sys
from PIL import Image, ImageFilter
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

from pic_board import tasks
# Create your models here.


class PicPost(models.Model):
    image = models.ImageField(upload_to='static/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    likes_count = models.PositiveBigIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)

    # def save(self, *args, **kwargs):
    #     # Open the uploaded image using Pillow
    #     img = Image.open(self.image)

    #     # Check the size of the image
    #     if self.image.size > 8 * 1024 * 1024:
    #         # Resize the image to be less than 8000x8000 pixels
    #         new_width = min(img.size[0], 8000)
    #         new_height = min(img.size[1], 8000)
    #         img.thumbnail((new_width, new_height), Image.BILINEAR)
    #         output = BytesIO()
    #         img.save(output, format='JPEG', quality=25)
    #         output.seek(0)

    #         # Overwrite the original image with the resized image
    #         self.image = InMemoryUploadedFile(
    #             output, 'ImageField', f"{self.image.name.split('/')[-1]}",
    #             'image/jpeg', sys.getsizeof(output), None
    #         )

    #     super().save(*args, **kwargs)



class LikePost(models.Model):
    """Stores number of likes on the post"""
    post = models.ForeignKey(PicPost, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'liked_by')



class CommentPost(models.Model):
    """Stores users comments on post"""
    content = models.CharField(max_length=500)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    post = models.ForeignKey(PicPost, on_delete=models.CASCADE, db_index=True)
    reply_to_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', db_index=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



@receiver(post_save, sender=PicPost)
def resize_image_on_post_save(sender, instance, created, **kwargs):
    if created:
        resized_image_path = tasks.resize_image.apply_async(args=[instance.image.path]).get()
        if resized_image_path:
            instance.image = resized_image_path
            instance.save()
