#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from core.models import User, Course, Semester

print("\n=== Database Content ===\n")

print("Courses:")
courses = Course.objects.all()
for c in courses:
    print(f"  {c.id}: {c.name}")

print("\nSemesters:")
semesters = Semester.objects.all()
for s in semesters:
    print(f"  {s.id}: {s.name}")

print("\nStudents:")
students = User.objects.filter(is_student=True)
for s in students:
    course_name = s.course.name if s.course else "No course"
    semester_name = s.semester.name if s.semester else "No semester"
    print(f"  {s.name}: {course_name}, {semester_name}")
