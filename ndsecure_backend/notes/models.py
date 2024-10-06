from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    has_been_read = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        return f"Note {self.id}"

class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.action} on {self.timestamp}"