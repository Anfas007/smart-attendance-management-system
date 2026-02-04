from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import json 
import numpy as np 

# -----------------------
# Core Management Models
# -----------------------

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True, help_text="Designates whether this department is currently active.")

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'department')

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Session(models.Model):
    year = models.CharField(max_length=50, unique=True, help_text="e.g., 2024-2025")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.year

class Semester(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., 1st Semester, Fall 2024")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# -----------------------
# Attendance Settings Model
# -----------------------

class AttendanceSettings(models.Model):
    """Single instance model for attendance time settings."""
    present_cutoff = models.TimeField(
        default='09:30',
        help_text="Students arriving before this time will be marked as Present"
    )
    late_cutoff = models.TimeField(
        default='11:00',
        help_text="Students arriving between present cutoff and this time will be marked as Late. After this time, they will be marked as Absent."
    )

    class Meta:
        verbose_name = 'Attendance Time Settings'
        verbose_name_plural = 'Attendance Time Settings'

    def clean(self):
        if self.present_cutoff >= self.late_cutoff:
            raise ValidationError({
                'late_cutoff': 'Late cutoff time must be after present cutoff time.'
            })

    def save(self, *args, **kwargs):
        if not self.pk and AttendanceSettings.objects.exists():
            raise ValidationError('There can only be one AttendanceSettings instance')
        return super(AttendanceSettings, self).save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the single instance of settings."""
        instance = cls.objects.first()
        if not instance:
            from datetime import time
            instance = cls.objects.create(
                present_cutoff=time(9, 30),
                late_cutoff=time(11, 0)
            )
        return instance

    def __str__(self):
        return f"Attendance Time Settings (Present until: {self.present_cutoff.strftime('%I:%M %p')}, Late until: {self.late_cutoff.strftime('%I:%M %p')})"

# -----------------------
# Main User Model
# -----------------------

class User(AbstractUser):
    # --- Role fields ---
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    authorized = models.BooleanField(default=False, help_text="Set to true when admin approves the student")
    is_active = models.BooleanField(default=True, help_text="Designates whether this user should be treated as active.") # Added is_active to User model


    # --- Student-specific Personal fields ---
    name = models.CharField(max_length=200, null=True, blank=True)
    roll_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    mother_name = models.CharField(max_length=200, null=True, blank=True)
    father_name = models.CharField(max_length=200, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True) 

    # --- Student-specific Academic fields (ForeignKeys) ---
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    # --- Face Recognition Field ---
    face_encoding = models.TextField(blank=True, null=True, help_text="JSON representation of the face encoding.")

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    # --- Methods to get/set encoding ---
    def get_encoding(self):
        """Retrieves the face encoding from the JSON string as a numpy array."""
        if self.face_encoding:
            try:
                # Use numpy array for compatibility with face_recognition
                return np.array(json.loads(self.face_encoding))
            except json.JSONDecodeError:
                print(f"Error decoding face encoding JSON for user {self.username}")
                return None
        return None

    def set_encoding(self, encoding):
        """Stores the face encoding (numpy array) as a JSON string and saves individual .npy file."""
        import os
        from django.conf import settings
        
        if encoding is not None:
            # Convert numpy array to list for JSON serialization
            self.face_encoding = json.dumps(encoding.tolist())
            
            # Save individual .npy file
            try:
                encodings_dir = os.path.join(settings.BASE_DIR, 'encodings')
                os.makedirs(encodings_dir, exist_ok=True)
                
                filename = f'student_{self.id}.npy'
                filepath = os.path.join(encodings_dir, filename)
                np.save(filepath, encoding)
                
                print(f"[Face Encoding] Saved .npy file: {filepath}")
            except Exception as e:
                print(f"[Face Encoding Error] Failed to save .npy file for student {self.username}: {e}")
        else:
            self.face_encoding = None

# -----------------------
# App-specific Models
# -----------------------

class Camera(models.Model):
    CAMERA_TYPES = [
        ('usb', 'USB Camera'),
        ('ip', 'IP Camera'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('offline', 'Offline'),
    ]

    name = models.CharField(max_length=100, unique=True)
    camera_type = models.CharField(max_length=10, choices=CAMERA_TYPES, default='usb')
    location = models.CharField(max_length=200, help_text="e.g., 'Main Entrance', 'Library Room 2'")
    ip_address = models.CharField(max_length=15, blank=True, null=True, help_text="Required for IP cameras")
    port = models.IntegerField(blank=True, null=True, help_text="Port for IP cameras")
    stream_url = models.URLField(blank=True, null=True, help_text="RTSP/HTTP stream URL for IP cameras")
    device_index = models.IntegerField(default=0, help_text="Camera device index for USB cameras (0, 1, 2, etc.)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    is_default = models.BooleanField(default=False, help_text="Default camera for attendance")
    resolution_width = models.IntegerField(default=640, help_text="Video resolution width")
    resolution_height = models.IntegerField(default=480, help_text="Video resolution height")
    fps = models.IntegerField(default=30, help_text="Frames per second")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.location})"

    def get_stream_url(self):
        """Get the appropriate stream URL based on camera type"""
        if self.camera_type == 'ip' and self.stream_url:
            return self.stream_url
        elif self.camera_type == 'usb':
            return f"device:{self.device_index}"
        return None

    def is_available(self):
        """Check if camera is available for use"""
        return self.status == 'active'

    def save(self, *args, **kwargs):
        # Ensure only one default camera
        if self.is_default:
            Camera.objects.filter(is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records', limit_choices_to={'is_student': True})
    date = models.DateField(default=timezone.now) 
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES) 
    manually_marked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests', limit_choices_to={'is_student': True})
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leaves')

    def __str__(self):
        return f"Leave for {self.student.username} ({self.start_date} to {self.end_date}) - {self.status}"
