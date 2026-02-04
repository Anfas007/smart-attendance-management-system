from django.core.management.base import BaseCommand
from core.models import AttendanceSettings
from datetime import time

class Command(BaseCommand):
    help = 'Initialize default attendance time settings'

    def handle(self, *args, **kwargs):
        if not AttendanceSettings.objects.exists():
            AttendanceSettings.objects.create(
                present_cutoff=time(9, 30),  # 9:30 AM
                late_cutoff=time(11, 0)      # 11:00 AM
            )
            self.stdout.write(self.style.SUCCESS('Successfully created default attendance settings'))
        else:
            self.stdout.write(self.style.SUCCESS('Attendance settings already exist'))