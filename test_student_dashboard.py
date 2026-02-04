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

def test_student_dashboard():
    """Test that student dashboard loads with the new modern design."""

    print("\n=== Testing Student Dashboard Design ===\n")

    # Create test student
    c = Client()
    if not User.objects.filter(username='teststudent').exists():
        User.objects.create_user(username='teststudent', password='testpass', is_student=True)

    # Login
    login_success = c.login(username='teststudent', password='testpass')
    print(f"Student login successful: {login_success}\n")

    # Test the student dashboard
    response = c.get('/student/dashboard/', HTTP_HOST='127.0.0.1')
    print(f'Student Dashboard Status Code: {response.status_code}')

    if response.status_code == 200:
        content = response.content.decode()

        # Check for new design elements
        print(f'Contains modern gradient background: {"gradient-bg" in content}')
        print(f'Contains glass effect styling: {"glass-effect" in content}')
        print(f'Contains glass card styling: {"glass-card" in content}')
        print(f'Contains animated background elements: {"animate-float" in content}')
        print(f'Contains hover lift effects: {"hover-lift" in content}')
        print(f'Contains modern navigation: {"Student Portal" in content}')
        print(f'Contains welcome header: {"Welcome back" in content}')
        print(f'Contains profile overview section: {"Profile Overview" in content}')
        print(f'Contains attendance overview: {"Attendance Overview" in content}')
        print(f'Contains quick actions: {"Apply for Leave" in content}')
        print(f'Contains modern stat cards: {"stat-card" in content}')

        print("\n=== Design Test Results ===")
        modern_elements = [
            "gradient-bg" in content,
            "glass-effect" in content,
            "glass-card" in content,
            "Student Portal" in content,
            "Welcome back" in content,
            "Profile Overview" in content,
            "Attendance Overview" in content,
            "stat-card" in content
        ]

        if all(modern_elements):
            print("✅ SUCCESS: Student dashboard has been successfully redesigned with modern elements")
        else:
            print("❌ FAILURE: Some modern design elements are missing")

    else:
        print(f"❌ ERROR: Dashboard failed to load (Status: {response.status_code})")
        print(f"Response: {response.content.decode()[:500]}")

if __name__ == '__main__':
    test_student_dashboard()