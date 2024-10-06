from django.contrib import admin
from .models import Note, AuditLog

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'has_been_read', 'created_by')
    list_filter = ('has_been_read', 'created_at')
    search_fields = ('id', 'created_by__username')
    readonly_fields = ('id', 'created_at')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'note', 'user', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('note__id', 'user__username', 'ip_address')
    readonly_fields = ('timestamp', 'note', 'user', 'ip_address')