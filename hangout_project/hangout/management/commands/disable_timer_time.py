from django.core.management.base import BaseCommand
from hangout.models import UserData
from hangout.general import disable_availability
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Disable availability on timer'

    def handle(self, *args, **options):
        users_data = UserData.objects.all()
        for user_data in users_data:
            timer = user_data.timer_disable_time
            current = datetime.today()
            left = relativedelta(timer, current)
            left_minutes = left.hours * 60 + left.minutes
            if left_minutes < 15:
                disable_availability(user_data)
