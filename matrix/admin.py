from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_quadrant', 'is_urgent', 'is_important', 'completed', 'created_at')
    list_filter = ('is_urgent', 'is_important', 'completed', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description')
        }),
        ('Priority', {
            'fields': ('is_urgent', 'is_important')
        }),
        ('Status', {
            'fields': ('completed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )