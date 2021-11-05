from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_finished', 'success']


admin.site.register(Task, TaskAdmin)
