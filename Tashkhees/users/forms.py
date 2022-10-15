from dataclasses import fields
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "full_name",
            "email",
            "password",
            "phone",
            "address",
            "city",
            "state",
            "zip_code",
            "nic_number",
            "gender",
            "age"
        )
