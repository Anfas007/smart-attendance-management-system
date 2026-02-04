from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AttendanceRecord, Camera, AttendanceSettings

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_admin', 'is_student', 'authorized')
    list_filter = ('is_admin', 'is_student', 'authorized')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_student', 'authorized', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_admin', 'is_student', 'authorized'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('username',)

# Register attendance and camera models
admin.site.register(AttendanceRecord)
admin.site.register(Camera)

@admin.register(AttendanceSettings)
class AttendanceSettingsAdmin(admin.ModelAdmin):
    list_display = ('present_cutoff', 'late_cutoff')
    readonly_fields = ('id',)
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not AttendanceSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return False
