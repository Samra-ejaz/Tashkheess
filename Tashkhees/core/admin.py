from django.contrib import admin

from core.models import Report, Meeting, KidneyStoneDetection

# Register your models here.
admin.site.register(Report)
admin.site.register(Meeting)
admin.site.register(KidneyStoneDetection)