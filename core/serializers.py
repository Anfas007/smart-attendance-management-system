from rest_framework import serializers
from .models import User, AttendanceRecord, Camera

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = ['id', 'date', 'check_in_time', 'check_out_time', 'status', 'manually_marked']

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['id', 'name', 'ip_address']

class StudentSerializer(serializers.ModelSerializer):
    attendance_summary = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','username','email','authorized','attendance_summary']

    def get_attendance_summary(self, obj):
        # requires obj.is_student = True
        records = obj.attendance_records.all()
        total = records.count()
        present = records.filter(status='present').count()
        absent = records.filter(status='absent').count()
        late = records.filter(status='late').count()
        return {
            'total': total,
            'present': present,
            'absent': absent,
            'late': late
        }
