import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
django.setup()

from django.utils import timezone
from django.template import Template, Context

# Test date formatting
today = timezone.now().date()
print('Today:', today)
print('Formatted:', today.strftime('%d/%m/%Y'))

# Test Django template
t = Template('{{ date|date:"d/m/Y" }}')
c = Context({'date': today})
result = t.render(c)
print('Django template result:', result)

# Test with different date
test_date = timezone.datetime(2025, 11, 4).date()
print('Test date:', test_date)
t2 = Template('{{ date|date:"d/m/Y" }}')
c2 = Context({'date': test_date})
result2 = t2.render(c2)
print('Test date result:', result2)