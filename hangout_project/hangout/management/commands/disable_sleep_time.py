from django.core.management.base import BaseCommand
from hangout.models import UserData
from hangout.general import disable_availability
from datetime import datetime


class Command(BaseCommand):
    help = 'Disable availability when sleep time reached'

    def handle(self, *args, **options):
        users_data = UserData.objects.all()
        for user_data in users_data:
            sleep_time = user_data.sleep_disable_time
            current_time = datetime.today()
            if sleep_time.hour == current_time.hour and sleep_time.minute == current_time.minute:
                disable_availability(user_data)
