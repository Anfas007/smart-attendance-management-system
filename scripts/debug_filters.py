import requests
from bs4 import BeautifulSoup

# Start Django server if not running
import subprocess
import time

# Login and get session
session = requests.Session()

# Login
login_data = {
    'username': 'admin',
    'password': 'admin123'
}
response = session.post('http://127.0.0.1:8000/login/', data=login_data)

print(f"Login status: {response.status_code}")

# Get the attendance page
response = session.get('http://127.0.0.1:8000/face_attendance/')

print(f"Page status: {response.status_code}")
print(f"Response length: {len(response.text)}")

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Check for filter elements
department_filter = soup.find('select', {'id': 'department'})
course_filter = soup.find('select', {'id': 'course_filter'})
session_filter = soup.find('select', {'id': 'session_filter'})
semester_filter = soup.find('select', {'id': 'semester'})

print(f"Department filter found: {department_filter is not None}")
print(f"Course filter found: {course_filter is not None}")
print(f"Session filter found: {session_filter is not None}")
print(f"Semester filter found: {semester_filter is not None}")

# Check for filter button
filter_button = soup.find('button', string=lambda text: 'Filter' in text if text else False)
print(f"Filter button found: {filter_button is not None}")

# Print the HTML around the filter section
filter_div = soup.find('div', class_='bg-gray-50')
if filter_div:
    print("Filter section HTML:")
    print(filter_div.prettify()[:2000])  # First 2000 chars
else:
    print("Filter section not found")

# Check for any Django error messages
if 'TemplateSyntaxError' in response.text or 'TemplateDoesNotExist' in response.text:
    print("Django template error detected!")
    # Find error details
    error_start = response.text.find('TemplateSyntaxError')
    if error_start != -1:
        error_end = response.text.find('</div>', error_start)
        print(response.text[error_start:error_end + 6])