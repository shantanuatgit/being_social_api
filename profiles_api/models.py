from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for the user profile"""
    def create_user(self, email, full_name, password=None):
        """create new user profile"""
        if not email:
            raise ValueError('User must have email address')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password):
        """create new superuser with given details"""
        user = self.create_user(email, full_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user



class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for the user in the system"""
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=225)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='static/', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveBigIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def get_full_name(self):
        """Retrieve full full_name of the user"""
        return self.full_name
    
    def get_short_name(self):
        """Retrieve short full_name of the user"""
        return self.full_name
    
    def __str__(self):
        """Return string representation of the user"""
        return self.email



class FollowerFollowing(models.Model):
    """Database model for user followers and following"""

    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leader')
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        unique_together = ('leader', 'follower')

    def __str__(self):
        return f"{self.follower} follow {self.leader}"