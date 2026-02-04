from django import template
from core.models import Course, Semester

register = template.Library()

@register.filter
def course_abbrev(course_name):
    """
    Convert long course names to abbreviated forms
    """
    if not course_name:
        return course_name

    # Course name abbreviations mapping
    abbreviations = {
        'Master of Science in Computer Science': 'MSc CS',
        'Master of Science in Information Technology': 'MSc IT',
        'Master of Science in Software Engineering': 'MSc SE',
        'Master of Science in Data Science': 'MSc DS',
        'Master of Science in Artificial Intelligence': 'MSc AI',
        'Master of Science in Machine Learning': 'MSc ML',
        'Bachelor of Science in Computer Science': 'BSc CS',
        'Bachelor of Science in Information Technology': 'BSc IT',
        'Bachelor of Science in Software Engineering': 'BSc SE',
        'Bachelor of Science in Electrical Engineering': 'BSc EE',
        'Bachelor of Science in Mechanical Engineering': 'BSc ME',
        'Bachelor of Science in Civil Engineering': 'BSc CE',
        'Bachelor of Technology in Computer Science': 'BTech CS',
        'Bachelor of Technology in Information Technology': 'BTech IT',
        'Bachelor of Technology in Electronics': 'BTech ECE',
        'Master of Technology in Computer Science': 'MTech CS',
        'Master of Technology in Information Technology': 'MTech IT',
        'Master of Business Administration': 'MBA',
        'Bachelor of Business Administration': 'BBA',
        'Doctor of Philosophy': 'PhD',
        'Master of Computer Applications': 'MCA',
        'Bachelor of Computer Applications': 'BCA',
    }

    # Check for exact matches first
    if course_name in abbreviations:
        return abbreviations[course_name]

    # Check for partial matches (contains)
    for long_name, short_name in abbreviations.items():
        if long_name.lower() in course_name.lower():
            return short_name

    # If no abbreviation found, return the original name (possibly truncated)
    return course_name

@register.filter
def get_course_name(course_id):
    """
    Get course name by ID
    """
    try:
        course = Course.objects.get(id=course_id)
        return course.name
    except (Course.DoesNotExist, ValueError):
        return "Unknown Course"

@register.filter
def get_semester_name(semester_id):
    """
    Get semester name by ID
    """
    try:
        semester = Semester.objects.get(id=semester_id)
        return semester.name
    except (Semester.DoesNotExist, ValueError):
        return "Unknown Semester"