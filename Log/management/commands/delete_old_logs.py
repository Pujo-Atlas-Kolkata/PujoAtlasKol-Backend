from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from Log.models import Log

class Command(BaseCommand):
    help = 'Delete log entries older than one week'

    def handle(self, *args, **kwargs):
        one_week_ago = timezone.now() - timedelta(weeks=1)
        Log.objects.filter(created_at__lt=one_week_ago).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted old log entries'))
