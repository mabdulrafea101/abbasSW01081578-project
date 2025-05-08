from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'manager')  # Set user_type to manager
        extra_fields.setdefault('is_account_confirmed', True)  # Set account as confirmed
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    email = models.EmailField(unique=True)  # Ensure email is unique
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    
    """
    Custom User model extending Django's AbstractUser.
    """

    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=20,
                                 choices=ROLE_CHOICES, blank= True, null= True)
    is_account_confirmed = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.'
        'A user will get all permissions granted to each of their groups.',
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
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # Points and leveling fields
    total_points = models.PositiveIntegerField(default=0)
    current_level = models.PositiveIntegerField(default=1)
    
    def get_level_thresholds(self):
        """Return the level thresholds as a list"""
        return [51, 101, 201, 401, 801]  # Upper bounds for each level
    
    def calculate_level(self):
        """Calculate the user's level based on their total points"""
        thresholds = self.get_level_thresholds()
        for level, threshold in enumerate(thresholds, 2):  # Start at level 2
            if self.total_points < threshold:
                return level - 1
        return len(thresholds) + 1  # If they exceed all thresholds
    
    def update_level(self):
        """Update the user's level based on their total points"""
        new_level = self.calculate_level()
        if new_level != self.current_level:
            old_level = self.current_level
            self.current_level = new_level
            self.save(update_fields=['current_level'])
            return old_level, new_level
        return None
    
    def add_points(self, points, reason=None):
        """Add points to the user and update their level"""
        self.total_points += points
        self.save(update_fields=['total_points'])
        level_change = self.update_level()
        
        # Create point history record
        PointHistory.objects.create(
            user=self.user,
            points=points,
            reason=reason,
            total_after=self.total_points
        )
        
        return level_change
    
    # Add the missing properties
    @property
    def points_needed_for_next_level(self):
        """Calculate how many points are needed to reach the next level"""
        thresholds = self.get_level_thresholds()
        if self.current_level <= len(thresholds):
            return thresholds[self.current_level - 1] - self.total_points
        return 0  # Max level reached
    
    @property
    def level_progress_percentage(self):
        """Calculate the percentage progress towards the next level"""
        if self.current_level > len(self.get_level_thresholds()):
            return 100  # Max level reached
            
        # Get current level threshold (points needed to reach current level)
        current_threshold = 0 if self.current_level == 1 else self.get_level_thresholds()[self.current_level - 2]
        
        # Get next level threshold
        next_threshold = self.get_level_thresholds()[self.current_level - 1]
        
        # Calculate points earned in current level and total points needed for current level
        points_in_level = self.total_points - current_threshold
        points_needed_for_level = next_threshold - current_threshold
        
        # Calculate percentage
        return min(100, int((points_in_level / points_needed_for_level) * 100))


# In user/models.py
class PointHistory(models.Model):
    """Track all point transactions for audit and history purposes"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='point_history')
    points = models.IntegerField()  # Can be positive or negative
    reason = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_after = models.PositiveIntegerField()  # Total points after this transaction
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Point histories"
    
    def __str__(self):
        return f"{self.user.username}: {self.points} points for {self.reason}"
