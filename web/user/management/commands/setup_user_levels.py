# In user/management/commands/setup_user_levels.py
from django.core.management.base import BaseCommand
from user.models import UserProfile, CustomUser

class Command(BaseCommand):
    help = 'Set up initial user levels based on current points'

    def handle(self, *args, **options):
        # Get all users with profiles
        users = CustomUser.objects.all()
        updated = 0
        
        for user in users:
            try:
                profile = user.profile
                old_level = profile.current_level
                profile.update_level()
                if old_level != profile.current_level:
                    updated += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Updated {user.username} from level {old_level} to {profile.current_level}"
                        )
                    )
            except UserProfile.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"User {user.username} has no profile, skipping")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"Updated levels for {updated} users")
        )
