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

def test_admin_dashboard():
    """Test that admin dashboard loads with the new mark attendance section."""
    
    print("\n=== Testing Admin Dashboard Changes ===\n")
    
    # Create test admin
    c = Client()
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_user(username='testadmin', password='testpass', is_admin=True)
    
    # Login
    login_success = c.login(username='testadmin', password='testpass')
    print(f"Admin login successful: {login_success}\n")
    
    # Test the admin dashboard
    response = c.get('/dashboard/', HTTP_HOST='127.0.0.1')
    print(f'Admin Dashboard Status Code: {response.status_code}')
    
    if response.status_code == 200:
        content = response.content.decode()
        
        # Check that the old charts are gone
        print(f'Contains old "Attendance Distribution" chart: {"Attendance Distribution" in content}')
        print(f'Contains old "Weekly Trends" chart: {"Weekly Trends" in content}')
        print(f'Contains chart canvas elements: {content.count("attendanceChart") + content.count("weeklyChart")}')
        
        # Check that the main statistics cards are removed
        print(f'Contains "Total Students" card: {"Total Students" in content}')
        print(f'Contains "Present Today" card: {"Present Today" in content}')
        print(f'Contains "Absent Today" card: {"Absent Today" in content}')
        print(f'Contains "Late Today" card: {"Late Today" in content}')
        print(f'Contains statistics cards grid: {content.count("grid-cols-1 sm:grid-cols-2 lg:grid-cols-4")}')
        
        # Check that the new mark attendance section is present
        print(f'Contains "Mark Attendance" section: {"Mark Attendance" in content}')
        print(f'Contains "Start Attendance" button: {"Start Attendance" in content}')
        print(f'Contains "Continue Session" button: {"Continue Session" in content}')
        print(f'Contains camera icon: {"camera" in content}')
        
        # Check for session status indicators
        print(f'Contains session status indicators: {"Attendance Session Active" in content or "No Active Session" in content}')
        
        # Check for quick stats (should be removed)
        print(f'Contains "Check-ins Today" stat: {"Check-ins Today" in content}')
        print(f'Contains "Present" stat: {"Present" in content and "Check-ins Today" not in content}')  # Make sure it's not just the status
        print(f'Contains "Active Cameras" stat: {"Active Cameras" in content}')
        print(f'Contains quick stats grid: {content.count("grid-cols-3")}')
        
        print("\n=== Test Results ===")
        if ("Mark Attendance" in content and 
            "Check-ins Today" not in content and 
            "Active Cameras" not in content and
            "Total Students" not in content and
            "Present Today" not in content and
            "Absent Today" not in content and
            "Late Today" not in content):
            print("✅ SUCCESS: Statistics cards and Quick Stats footer removed from dashboard")
        else:
            print("❌ FAILURE: Statistics cards or Quick Stats footer still present or other issues")
            
    else:
        print(f"❌ ERROR: Dashboard failed to load (Status: {response.status_code})")
        print(f"Response: {response.content.decode()[:500]}")

if __name__ == '__main__':
    test_admin_dashboard()