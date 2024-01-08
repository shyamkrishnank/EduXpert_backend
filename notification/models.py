from django.db import models
from auth_app.models import UserAccount
import uuid


class NotificationRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=300)


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255, default='message')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    room = models.ForeignKey(NotificationRoom, on_delete=models.CASCADE, default=None)