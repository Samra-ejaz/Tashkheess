from django import forms
from .models import Report, Meeting
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class MeetingForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(user_type="DR"))
    datetime = forms.CharField()
    reason = forms.CharField(widget=forms.Textarea())

    def save(self, user, commit=True):
        date_time = self.cleaned_data.pop("datetime")
        received_datetime = datetime.strptime(date_time, "%Y/%m/%d %H:%M")
        instance = Meeting(
            **self.cleaned_data,
            patient=user,
            date_time=received_datetime,
        )
        if commit:
            instance.save()
        return instance


class ReportForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.filter(user_type="PT"))

    class Meta:
        model = Report
        exclude = ("uploaded_by",)

    def save(self, request, commit=True):
        instance = Report(
            **self.cleaned_data,
            uploaded_by=request.user,
        )

        if commit:
            instance.save()
        return instance


class KidneyImageUploadForm(forms.Form):
    image = forms.ImageField()
