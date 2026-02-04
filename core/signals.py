from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if instance.is_student:
        if created:
            StudentProfile.objects.create(user=instance)
        else:
            instance.student_profile.save()
