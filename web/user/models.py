from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    email = models.EmailField(unique=True)  # Ensure email is unique
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    """
    Custom User model extending Django's AbstractUser.
    """

    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=20,
                                 choices=ROLE_CHOICES,)
    is_account_confirmed = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",  # Add a unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Add a unique related_name
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    Profile model linked to the CustomUser model.
    """
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='profile')
    total_points = models.PositiveIntegerField(default=0)
    current_level = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True,
                                        null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_level(self):
        """
        Update the user's level based on their total points.
        """
        LEVELS = [10, 30, 50, 100, 200]
        for idx, threshold in enumerate(LEVELS):
            if self.total_points >= threshold:
                self.current_level = idx + 1
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Profile"