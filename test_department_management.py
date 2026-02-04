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
from core.models import Department
User = get_user_model()

def test_department_management():
    c = Client()

    # Check database content
    print("Database content:")
    print(f"Departments: {Department.objects.count()}")

    # Create a test admin user if it doesn't exist
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_user(username='testadmin', password='testpass', is_admin=True)

    # Login
    login_success = c.login(username='testadmin', password='testpass')
    print(f"Login successful: {login_success}")

    # Test the manage_departments view
    response = c.get('/dashboard/departments/', HTTP_HOST='127.0.0.1')
    print(f'Manage Departments Status Code: {response.status_code}')

    if response.status_code == 200:
        content = response.content.decode()
        print(f'Contains department table: {"manage_departments" in content}')
        print(f'Contains edit button: {"edit_department" in content}')
        print(f'Contains delete button: {"delete_department" in content}')
        print(f'Contains disabled buttons: {"cursor-not-allowed" in content}')

        # Check for action buttons
        print(f'Contains action buttons: {content.count("edit-2") + content.count("trash-2")}')

        # Print a portion of the HTML to see what's actually rendered
        print("\nFirst 1000 characters of response:")
        print(content[:1000])

    else:
        print(f"Error response: {response.content.decode()[:500]}")

if __name__ == '__main__':
    test_department_management()