from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("patients/", patient_list, name="patient_list"),
    path("patients/<int:id>/", patient_detail, name="patient_detail"),
    path("reports/", reports_list, name="reports_list"),
    path("reports/<uuid:uuid>/", report_detail, name="report_detail"),
    path("reports/new/", ReportFormView.as_view(), name="report_new"),
    path("arrange_meeting/", ArrangeMeetingView.as_view(), name="arrange_meeting"),
    path("meetings/", meetings, name="meetings"),
    path("detect_kidney_stones/", detect_kidney_stones, name="detect_kidney_stones"),
]
