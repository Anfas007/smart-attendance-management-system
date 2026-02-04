#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from core.models import Department, Course, Session, Semester
User = get_user_model()

def test_attendance_details_view():
    c = Client()

    # Check database content
    print("Database content:")
    print(f"Departments: {Department.objects.count()}")
    print(f"Courses: {Course.objects.count()}")
    print(f"Sessions: {Session.objects.count()}")
    print(f"Semesters: {Semester.objects.count()}")
    print(f"Students: {User.objects.filter(is_student=True).count()}")

    # Create a test admin user if it doesn't exist
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_user(username='testadmin', password='testpass', is_admin=True)

    # Login
    login_success = c.login(username='testadmin', password='testpass')
    print(f"Login successful: {login_success}")

    # Test the attendance_details view without any session data
    response = c.get('/dashboard/attendance-details/', HTTP_HOST='127.0.0.1')
    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        content = response.content.decode()
        print(f'Contains department filter: {"department" in content}')
        print(f'Contains course filter: {"course" in content}')
        print(f'Contains semester filter: {"semester" in content}')
        print(f'Contains session filter: {"session" in content}')
        print(f'Contains filter button: {"Filter" in content}')

        # Check that there are no pre-selected values (no "selected_course" or "selected_semester" in context)
        print(f'Contains "selected_course": {"selected_course" in content}')
        print(f'Contains "selected_semester": {"selected_semester" in content}')

        # Check for select elements
        print(f'Contains select elements: {content.count("<select")}')

        # Print a portion of the HTML to see what's actually rendered
        print("\nFirst 1000 characters of response:")
        print(content[:1000])

    else:
        print(f"Error response: {response.content.decode()[:500]}")

if __name__ == '__main__':
    test_attendance_details_view()