from django.urls import path
from . import views

urlpatterns = [
    # -----------------------
    # General Views
    # -----------------------
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # -----------------------
    # Admin Dashboard & Management Views
    # -----------------------
    # Main Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Student Management
    path('dashboard/register/', views.register_student, name='register_student'),
    path('dashboard/students/', views.manage_students_view, name='manage_students'),
    path('dashboard/students/edit/<int:user_id>/', views.edit_student_view, name='edit_student'),
    path('dashboard/authorize-student/<int:user_id>/', views.authorize_student, name='authorize_student'),
    path('dashboard/delete-student/<int:user_id>/', views.delete_student, name='delete_student'), # POST

    # Academic Management
    path('dashboard/courses/', views.manage_courses_view, name='manage_courses'),
    path('dashboard/courses/add/', views.add_course_view, name='add_course'),
    path('dashboard/courses/edit/<int:course_id>/', views.edit_course_view, name='edit_course'),
    path('dashboard/courses/delete/<int:course_id>/', views.delete_course_view, name='delete_course'), # POST

    path('dashboard/departments/', views.manage_departments_view, name='manage_departments'),
    path('dashboard/departments/add/', views.add_department_view, name='add_department'),
    path('dashboard/departments/edit/<int:department_id>/', views.edit_department_view, name='edit_department'),
    path('dashboard/departments/delete/<int:department_id>/', views.delete_department_view, name='delete_department'), # POST

    path('dashboard/sessions/', views.manage_sessions_view, name='manage_sessions'),
    path('dashboard/sessions/add/', views.add_session_view, name='add_session'),
    path('dashboard/sessions/edit/<int:session_id>/', views.edit_session_view, name='edit_session'),
    path('dashboard/sessions/delete/<int:session_id>/', views.delete_session_view, name='delete_session'), # POST

    path('dashboard/semesters/', views.manage_semesters_view, name='manage_semesters'),
    path('dashboard/semesters/add/', views.add_semester_view, name='add_semester'),
    path('dashboard/semesters/edit/<int:semester_id>/', views.edit_semester_view, name='edit_semester'),
    path('dashboard/semesters/delete/<int:semester_id>/', views.delete_semester_view, name='delete_semester'), # POST

    # Attendance & Leave Management
    path('dashboard/attendance-details/', views.attendance_details_view, name='attendance_details'),
    path('dashboard/attendance-details/download/', views.download_attendance_report, name='download_attendance_report'),
    path('dashboard/leave-requests/', views.manage_leave_view, name='manage_leave'),
    path('dashboard/notify/', views.notify_absent_or_late, name='notify'),

    # --- Face Recognition (Mark Attendance) ---
    path('dashboard/face-attendance/', views.face_attendance_view, name='face_attendance'), 
    path('dashboard/recognize-face/', views.recognize_face_view, name='recognize_face'), # API endpoint
    path('dashboard/checkout-student/', views.checkout_student_view, name='checkout_student'), # Checkout API endpoint

    # Other Management
    path('dashboard/cameras/', views.manage_cameras_view, name='manage_cameras'),
    path('dashboard/cameras/add/', views.add_camera_view, name='add_camera'),
    path('dashboard/cameras/edit/<int:camera_id>/', views.edit_camera_view, name='edit_camera'),
    path('dashboard/cameras/delete/<int:camera_id>/', views.delete_camera_view, name='delete_camera'), # POST
    path('dashboard/cameras/toggle/<int:camera_id>/', views.toggle_camera_status, name='toggle_camera'), # POST
    path('dashboard/cameras/set-default/<int:camera_id>/', views.set_default_camera, name='set_default_camera'), # POST
    path('dashboard/cameras/test/<int:camera_id>/', views.test_camera_connection, name='test_camera'), # POST

    path('dashboard/end-attendance-session/', views.end_attendance_session_view, name='end_attendance_session'), # POST

    # -----------------------
    # Student Views
    # -----------------------
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/attendance/', views.attendance_view, name='attendance'),
    path('student/courses/', views.courses_view, name='courses'),
    path('student/leave/', views.apply_leave_view, name='apply_leave'),
    path('student/leave-status/', views.leave_status_view, name='leave_status'),
]
