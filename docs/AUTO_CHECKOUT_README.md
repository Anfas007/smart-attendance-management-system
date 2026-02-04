# Auto Checkout System

## Overview
The attendance system now includes an automatic checkout feature that ensures students who forget to manually check out are automatically checked out after a specified period.

## How It Works

### Current Behavior
- Students check in using face recognition during attendance sessions
- Students can manually check out using the checkout feature
- If a student doesn't check out manually, their checkout time remains **blank**
- After 1 day (24 hours), the system automatically checks out the student at 11:59 PM

### Automatic Checkout Process
1. **Daily Execution**: The auto-checkout command runs daily at midnight via cron job
2. **Detection**: Identifies attendance records that have check-in time but no checkout time
3. **Age Check**: Only processes records that are at least 1 day old
4. **Auto Checkout**: Sets checkout time to 11:59 PM for eligible records
5. **Logging**: Records all actions in the log file

## Configuration

### Cron Job Setup
The system uses a cron job to run the auto-checkout command daily:

```bash
# Run daily at midnight
0 0 * * * cd /path/to/your/project && python manage.py auto_checkout --days=1 --checkout-time=23:59 >> /path/to/your/project/logs/auto_checkout.log 2>&1
```

### Command Options
- `--days`: Number of days after check-in to auto-checkout (default: 1)
- `--checkout-time`: Default checkout time in HH:MM format (default: 23:59)

### Manual Execution
You can also run the command manually:

```bash
# Default behavior (1 day, 11:59 PM)
python manage.py auto_checkout

# Custom settings
python manage.py auto_checkout --days=2 --checkout-time=18:00
```

## Benefits

1. **Accurate Records**: Ensures all attendance records have complete check-in and checkout times
2. **Fair Calculation**: Prevents inflated attendance duration for students who forget to check out
3. **Automated Process**: No manual intervention required
4. **Flexible Configuration**: Can be adjusted based on institutional needs

## Database Impact

- **Before**: Records with blank checkout times
- **After**: All records have complete check-in and checkout times
- **Status**: No change to attendance status (Present/Absent/Late)
- **Duration**: Accurate calculation of time spent becomes possible

## Monitoring

Check the log file for auto-checkout activities:
```bash
tail -f /path/to/your/project/logs/auto_checkout.log
```

## Example Output
```
Searching for attendance records from 2025-11-10 or earlier that still have no checkout time...
Auto-checked out: John Doe (Roll: 12345) for 2025-11-09 at 11:59 PM
Auto-checked out: Jane Smith (Roll: 12346) for 2025-11-10 at 11:59 PM
Auto-checkout completed:
  - Records found: 2
  - Successfully checked out: 2
  - Skipped (already checked out): 0
  - Cutoff date: 2025-11-10
  - Default checkout time: 11:59 PM
```</content>
<parameter name="filePath">d:\temp\attendance_dashboard\AUTO_CHECKOUT_README.md