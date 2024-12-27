from django.contrib import admin

from tasks.models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('content', 'completed', 'created_at', 'user')
    