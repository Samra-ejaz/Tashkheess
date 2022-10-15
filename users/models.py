from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.core.validators import MaxValueValidator


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "ML", "Male"
        FEMALE = "FM", "Female"

    class UserTypeChoice(models.TextChoices):
        DOCTOR = "DR", "Doctor"
        PATIENT = "PT", "Patient"

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField()
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    nic_number = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999999)]
    )
    gender = models.CharField(
        max_length=2, choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    user_type = models.CharField(
        max_length=2, choices=UserTypeChoice.choices, default=UserTypeChoice.PATIENT
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["full_name", "phone", "nic_number", "gender", "age", "user_type"]

    def __str__(self):
        return self.username
