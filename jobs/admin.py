from django.contrib import admin

from .models import AllocatedJob, MALRequirement, MicroTask


@admin.register(MicroTask)
class MicroTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_selected', 'is_allocated', 'timestamp']
    list_filter = ['is_selected']
    search_fields = ['name']
    exclude = ['is_selected', 'is_allocated']


@admin.register(AllocatedJob)
class AllocatedJobAdmin(admin.ModelAdmin):
    list_display = ['job', 'outsource_email', 'time_allocated', 'time_completed']
    search_fields = ['job', 'outsource_email']


admin.site.register(MALRequirement)