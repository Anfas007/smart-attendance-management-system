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
User = get_user_model()

def test_student_registration_form():
    """Test that student registration form loads without the removed fields."""

    print("\n=== Testing Student Registration Form Changes ===\n")

    # Create test admin
    c = Client()
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_user(username='testadmin', password='testpass', is_admin=True)

    # Login
    login_success = c.login(username='testadmin', password='testpass')
    print(f"Admin login successful: {login_success}\n")

    # Test the student registration form
    response = c.get('/dashboard/register/', HTTP_HOST='127.0.0.1')
    print(f'Student Registration Form Status Code: {response.status_code}')

    if response.status_code == 200:
        content = response.content.decode()

        # Check that the form loads
        print(f'Contains registration form: {"Register New Student" in content}')

        # Check that removed fields are NOT present
        mothers_name = "Mother's Name"
        fathers_name = "Father's Name"
        print(f'Contains Date of Birth field: {"Date of Birth" in content}')
        print(f'Contains Mother\'s Name field: {mothers_name in content}')
        print(f'Contains Father\'s Name field: {fathers_name in content}')
        print(f'Contains Address field: {"Address" in content}')
        print(f'Contains Joining Date field: {"Joining Date" in content}')

        # Check that required fields are still present
        print(f'Contains Full Name field: {"Full Name" in content}')
        print(f'Contains Roll Number field: {"Roll Number" in content}')
        print(f'Contains Contact Number field: {"Contact Number" in content}')
        print(f'Contains Department field: {"Department" in content}')
        print(f'Contains Course field: {"Course" in content}')
        print(f'Contains Session field: {"Session" in content}')
        print(f'Contains Semester field: {"Semester" in content}')
        print(f'Contains Username field: {"Username" in content}')
        print(f'Contains Email field: {"Email" in content}')
        print(f'Contains Password field: {"Password" in content}')

        print("\n=== Form Test Results ===")
        removed_fields_present = any([
            "Date of Birth" in content,
            "Mother's Name" in content,
            "Father's Name" in content,
            "Address" in content,
            "Joining Date" in content
        ])

        required_fields_present = all([
            "Full Name" in content,
            "Roll Number" in content,
            "Contact Number" in content,
            "Department" in content,
            "Course" in content,
            "Session" in content,
            "Semester" in content,
            "Username" in content,
            "Email" in content,
            "Password" in content
        ])

        if not removed_fields_present and required_fields_present:
            print("✅ SUCCESS: Student registration form has been updated correctly - removed fields are gone and required fields remain")
        else:
            print("❌ FAILURE: Form changes are not correct")

    else:
        print(f"❌ ERROR: Form failed to load (Status: {response.status_code})")
        print(f"Response: {response.content.decode()[:500]}")

if __name__ == '__main__':
    test_student_registration_form()