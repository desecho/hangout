from django.core.management.base import BaseCommand
from hangout.models import Visibility, UserData


class Command(BaseCommand):
    help = 'Updates visibility when new user registers'

    def handle(self, *args, **options):
        users_data = UserData.objects.all()
        for user_data in users_data:
            friends_data = UserData.objects.exclude(user=user_data.user)
            for friend_data in friends_data:
                if not Visibility.objects.filter(user=user_data.user, friend=friend_data.user).exists():
                    Visibility(user=user_data.user, friend=friend_data.user).save()