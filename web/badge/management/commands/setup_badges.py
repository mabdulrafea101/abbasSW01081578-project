
# In badge/management/commands/setup_badges.py
from django.core.management.base import BaseCommand
from badge.models import BadgeType

class Command(BaseCommand):
    help = 'Sets up the initial badge types for the system'

    def handle(self, *args, **options):
        # Organizer Badges
        organizer_badges = [
            {
                'name': 'Novice Organizer',
                'description': 'Host 5 events → Unlocks a "Hosting Starter Kit" (custom event templates)',
                'icon': '🌱',
                'category': 'organizer',
                'level': 1,
                'requirement_count': 5
            },
            {
                'name': 'Bronze Organizer',
                'description': 'Host 10 events → Earns a "Featured Event" slot on the homepage',
                'icon': '🥉',
                'category': 'organizer',
                'level': 2,
                'requirement_count': 10
            },
            {
                'name': 'Silver Organizer',
                'description': 'Host 20 events → Gains access to advanced analytics tools',
                'icon': '🥈',
                'category': 'organizer',
                'level': 3,
                'requirement_count': 20
            },
            {
                'name': 'Gold Organizer',
                'description': 'Host 30 events → Receives a "Top Host" trophy + Scorun points bonus',
                'icon': '🥇',
                'category': 'organizer',
                'level': 4,
                'requirement_count': 30
            },
        ]
        
        # Participant Badges
        participant_badges = [
            {
                'name': 'Event Newcomer',
                'description': 'Attend 5 events → Unlocks a "Welcome Helper" badge',
                'icon': '🎫',
                'category': 'participant',
                'level': 1,
                'requirement_count': 5
            },
            {
                'name': 'Active Participant',
                'description': 'Attend 10 events → Earns priority registration for popular events',
                'icon': '🎟️',
                'category': 'participant',
                'level': 2,
                'requirement_count': 10
            },
            {
                'name': 'Event Enthusiast',
                'description': 'Attend 20 events → Gets a "VIP Participant" role in events',
                'icon': '🏅',
                'category': 'participant',
                'level': 3,
                'requirement_count': 20
            },
            {
                'name': 'Event Champion',
                'description': 'Attend 30 events → Wins a "Campus Star" title + exclusive perks',
                'icon': '🏆',
                'category': 'participant',
                'level': 4,
                'requirement_count': 30
            },
        ]
        
        # Helper Badges
        helper_badges = [
            {
                'name': 'Event Helper',
                'description': 'Rate 5 organizers → Earns a "Feedback Friend" badge',
                'icon': '🌟',
                'category': 'helper',
                'level': 1,
                'requirement_count': 5
            },
            {
                'name': 'Feedback Pro',
                'description': 'Rate 10 organizers → Unlocks a "Trusted Reviewer" tag',
                'icon': '💡',
                'category': 'helper',
                'level': 2,
                'requirement_count': 10
            },
            {
                'name': 'Rating Expert',
                'description': 'Rate 20 organizers → Gains double points for ratings for 1 week',
                'icon': '🎯',
                'category': 'helper',
                'level': 3,
                'requirement_count': 20
            },
            {
                'name': 'Master Evaluator',
                'description': 'Rate 30 organizers → Receives a "Rating Legend" badge + leaderboard feature',
                'icon': '💎',
                'category': 'helper',
                'level': 4,
                'requirement_count': 30
            },
        ]
        
        # Combine all badges
        all_badges = organizer_badges + participant_badges + helper_badges
        created_count = 0
        
        for badge_data in all_badges:
            badge, created = BadgeType.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            
            if created:
                created_count += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully set up {created_count} new badge types')
        )
