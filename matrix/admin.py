from django.contrib import admin
from .models import Task, Matrix, MatrixAccess

@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Matrix Information', {
            'fields': ('title', 'description', 'owner')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MatrixAccess)
class MatrixAccessAdmin(admin.ModelAdmin):
    list_display = ('matrix', 'user', 'created_at')
    list_filter = ('matrix', 'user', 'created_at')
    search_fields = ('matrix__title', 'user__username')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Access Information', {
            'fields': ('matrix', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'matrix', 'get_quadrant', 'is_urgent', 'is_important', 'completed', 'created_at')
    list_filter = ('matrix', 'is_urgent', 'is_important', 'completed', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'matrix', 'created_by')
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