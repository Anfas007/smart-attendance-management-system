from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin


class AttendanceSessionMiddleware(MiddlewareMixin):
    """
    Middleware to enforce attendance session security.
    When an admin starts an attendance session, they are locked into that page
    and must re-authenticate to access other admin pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that are allowed during attendance session
        self.allowed_urls = [
            '/login/',
            '/logout/',
            '/dashboard/face-attendance/',
            '/dashboard/recognize-face/',
            '/dashboard/checkout-student/',
            '/dashboard/end-attendance-session/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        # Check if user is authenticated and is admin
        if request.user.is_authenticated and request.user.is_admin:
            # Check if attendance session is active
            attendance_session_active = request.session.get('attendance_session_active', False)

            if attendance_session_active:
                # Check if current URL is allowed during attendance session
                current_path = request.path_info

                # Allow exact matches and prefixes for static/media
                is_allowed = any(
                    current_path.startswith(allowed) if allowed.endswith('/') else current_path == allowed
                    for allowed in self.allowed_urls
                )

                if not is_allowed:
                    # Force logout and redirect to login
                    logout(request)
                    messages.warning(request,
                        "Attendance session was active. Please log in again to access other admin features.")
                    return redirect(reverse('login'))

        response = self.get_response(request)
        return response