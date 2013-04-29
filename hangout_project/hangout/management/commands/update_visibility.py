from django.core.management.base import BaseCommand
from hangout.models import Visibility

class Command(BaseCommand):
    help = 'Updates visibility'

    def handle(self, *args, **options):
        visibilities = Visibility.objects.all()
        for visibility in visibilities:
            visibility.visible = visibility.visible_updated
            visibility.save()
