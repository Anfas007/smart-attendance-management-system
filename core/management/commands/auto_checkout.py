from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from core.models import AttendanceRecord
from datetime import time, timedelta

class Command(BaseCommand):
    help = 'Automatically check out students who have not checked out after a day'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=1,
            help='Number of days after check-in to auto-checkout (default: 1)',
        )
        parser.add_argument(
            '--checkout-time',
            type=str,
            default='23:59',
            help='Default checkout time in HH:MM format (default: 23:59)',
        )

    def handle(self, *args, **options):
        days_threshold = options['days']
        checkout_time_str = options['checkout_time']

        # Parse checkout time
        try:
            hours, minutes = map(int, checkout_time_str.split(':'))
            default_checkout_time = time(hours, minutes)
        except ValueError:
            self.stdout.write(
                self.style.ERROR(f'Invalid checkout time format: {checkout_time_str}. Use HH:MM format.')
            )
            return

        # Calculate the cutoff date (records older than this will be auto-checked out)
        cutoff_date = timezone.localdate() - timedelta(days=days_threshold)

        self.stdout.write(
            f'Searching for attendance records from {cutoff_date} or earlier that still have no checkout time...'
        )

        # Get all attendance records that:
        # 1. Have check-in time but no check-out time
        # 2. Are from days_threshold days ago or earlier
        # 3. Are not manually marked (to avoid overriding manual entries)
        records_to_checkout = AttendanceRecord.objects.filter(
            check_in_time__isnull=False,
            check_out_time__isnull=True,
            date__lte=cutoff_date,
            manually_marked=False
        ).select_related('student')

        updated_count = 0
        skipped_count = 0

        for record in records_to_checkout:
            # Double-check that checkout time is still null (in case of concurrent updates)
            if record.check_out_time is None:
                record.check_out_time = default_checkout_time
                record.save(update_fields=['check_out_time'])
                updated_count += 1

                self.stdout.write(
                    f'Auto-checked out: {record.student.name} (Roll: {record.student.roll_no}) '
                    f'for {record.date} at {default_checkout_time.strftime("%I:%M %p")}'
                )
            else:
                skipped_count += 1

        # Summary
        total_found = records_to_checkout.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Auto-checkout completed:\n'
                f'  - Records found: {total_found}\n'
                f'  - Successfully checked out: {updated_count}\n'
                f'  - Skipped (already checked out): {skipped_count}\n'
                f'  - Cutoff date: {cutoff_date}\n'
                f'  - Default checkout time: {default_checkout_time.strftime("%I:%M %p")}'
            )
        )

        # Additional statistics
        if updated_count > 0:
            # Show breakdown by date
            date_stats = {}
            updated_records = AttendanceRecord.objects.filter(
                check_in_time__isnull=False,
                check_out_time=default_checkout_time,
                date__lte=cutoff_date,
                manually_marked=False
            ).values('date').annotate(count=models.Count('id'))

            self.stdout.write('\nBreakdown by date:')
            for stat in updated_records:
                self.stdout.write(
                    f'  {stat["date"]}: {stat["count"]} students auto-checked out'
                )