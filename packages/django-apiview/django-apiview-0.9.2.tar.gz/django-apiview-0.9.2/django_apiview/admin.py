from django.contrib import admin
from .models import ApiResponseTimeLog


class ApiResponseTimeLogAdmin(admin.ModelAdmin):
    list_display = ["pk", "path", "response_time", "add_time"]
    list_filter = ["path"]
    ordering = ["add_time"]

admin.site.register(ApiResponseTimeLog, ApiResponseTimeLogAdmin)

