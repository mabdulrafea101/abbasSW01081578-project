# In /Users/mabdulrafea/Projects/hareem tasks/abbas_fyp/project/web/user/management/commands/create_missing_profiles.py

from django.core.management.base import BaseCommand
from user.models import CustomUser, Profile


class Command(BaseCommand):
    help = 'Create profiles for users that don\'t have them'

    def handle(self, *args, **options):
        # Get all users
        users = CustomUser.objects.all()
        count = 0
        
        for user in users:
            try:
                # Try to access profile
                profile = user.profile
            except Profile.RelatedObjectDoesNotExist:
                # Create profile if it doesn't exist
                Profile.objects.create(user=user)
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created profile for user {user.username}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"Created {count} profiles")
        )
