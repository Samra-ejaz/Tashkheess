from tokenize import blank_re
from django.conf import settings
from django.db import models

# from django.core.validators import MaxValueValidator
import uuid

# from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse

# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
# from django.core.files.base import ContentFile
# from PIL import Image as PIL_Image

# Create your models here.


class Meeting(models.Model):
    patient = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="patient_meetings"
    )
    doctor = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="doctor_meetings"
    )
    date_time = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.patient} - {self.doctor}"


class Report(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    patient = models.ForeignKey(
        "users.User", related_name="reports", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="reports/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="my_reports", on_delete=models.CASCADE
    )
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Repors"
        verbose_name_plural = "Reportes"
        ordering = ["-date_time"]

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs) -> None:
    #     color_image = PIL_Image.open(self.image)
    #     bw_image = color_image.convert("L")
    #     buffer = BytesIO()
    #     bw_image.save(buffer, format="JPEG")
    #     final_img = ContentFile(buffer.getvalue())
    #     self.image = SimpleUploadedFile(
    #         self.image.name, final_img.read(), content_type="image/jpeg"
    #     )
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("report_detail", kwargs={"uuid": self.uuid})


class KidneyStoneDetection(models.Model):
    orignal_image = models.ImageField(upload_to="kidney_stones/")
    processed_image = models.ImageField(upload_to="kidney_stones/", blank=True, null=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="my_kidney_stones",
        on_delete=models.CASCADE,
    )
    date_time = models.DateTimeField(auto_now_add=True)
    is_stone_detected = models.BooleanField(default=False)
    number_of_stones = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.uploaded_by} - {self.date_time}"
