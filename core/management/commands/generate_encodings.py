import face_recognition
import os
import json
import numpy as np
from PIL import Image, ImageOps
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import User

# Optional: Support HEIC images (does NOT break if not installed)
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except:
    pass


class Command(BaseCommand):
    help = 'Generates and saves face encodings for students with profile images.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Starting face encoding generation..."))

        students_to_process = User.objects.filter(
            is_student=True,
            authorized=True,
            profile_image__isnull=False
        ).exclude(profile_image='')

        processed_count = 0
        skipped_count = 0
        error_count = 0

        if not students_to_process.exists():
            self.stdout.write(self.style.WARNING("No students found with profile images to process."))
            return

        self.stdout.write(f"Found {students_to_process.count()} students with profile images.")

        for student in students_to_process:
            self.stdout.write(f"Processing student: {student.username} (ID: {student.id})... ")

            if not student.profile_image or not hasattr(student.profile_image, 'path'):
                self.stdout.write(self.style.WARNING("  No valid image path found, skipping."))
                skipped_count += 1
                continue

            image_path = student.profile_image.path

            if not os.path.exists(image_path):
                self.stdout.write(self.style.ERROR(f"  Image file not found at {image_path}, skipping."))
                error_count += 1
                continue

            try:
                # Load image and fix EXIF rotation (mobile photo issues)
                pil_image = Image.open(image_path)
                pil_image = ImageOps.exif_transpose(pil_image)

                # Force convert to 8-bit RGB
                if pil_image.mode != 'RGB':
                    pil_image = pil_image.convert("RGB")

                # Resize if image is too large (helps with detection)
                max_dimension = 1600
                if max(pil_image.size) > max_dimension:
                    self.stdout.write(f"  Resizing from {pil_image.size}... ")
                    pil_image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)

                # Use face_recognition's built-in image loader instead
                # This ensures proper format for dlib
                # Save to temp location and reload
                temp_path = image_path + ".temp.jpg"
                try:
                    pil_image.save(temp_path, "JPEG", quality=95)
                    image_array = face_recognition.load_image_file(temp_path)
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                self.stdout.write(f"  Image shape: {image_array.shape}, dtype: {image_array.dtype}")

                # Try HOG model first (faster)
                self.stdout.write("  Detecting faces (HOG)... ")
                face_locations = face_recognition.face_locations(
                    image_array, 
                    model='hog',
                    number_of_times_to_upsample=1
                )

                # If no faces found with HOG, try CNN (more accurate but slower)
                if not face_locations:
                    self.stdout.write("  No faces with HOG, trying CNN... ")
                    face_locations = face_recognition.face_locations(
                        image_array,
                        model='cnn'
                    )

                # If still no faces, try with more upsampling
                if not face_locations:
                    self.stdout.write("  Trying with increased upsampling... ")
                    face_locations = face_recognition.face_locations(
                        image_array,
                        model='hog',
                        number_of_times_to_upsample=2
                    )

                if face_locations:
                    self.stdout.write(f"  Found {len(face_locations)} face(s)")
                    
                    # Generate encodings for detected faces
                    encodings = face_recognition.face_encodings(image_array, face_locations)
                    
                    if encodings:
                        # Use the first face found
                        encoding = encodings[0]
                        student.set_encoding(encoding)
                        student.save(update_fields=['face_encoding'])
                        self.stdout.write(self.style.SUCCESS("  ✅ Encoding generated and saved."))
                        processed_count += 1
                    else:
                        self.stdout.write(self.style.WARNING("  ⚠️ Face detected but encoding failed, skipping."))
                        skipped_count += 1
                else:
                    self.stdout.write(self.style.WARNING("  ⚠️ No face detected after all attempts, skipping."))
                    skipped_count += 1

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"  ❌ Critical error for {student.username}: {e}"))
                import traceback
                self.stderr.write(traceback.format_exc())
                error_count += 1

        self.stdout.write(self.style.SUCCESS("\nFinished processing."))
        self.stdout.write(f"✅ Successfully generated/saved: {processed_count}")
        self.stdout.write(f"⚠️ Skipped (no face/no image path): {skipped_count}")
        self.stdout.write(f"❌ Errors: {error_count}")