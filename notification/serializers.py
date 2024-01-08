from rest_framework import serializers
from .models import NotificationRoom,Notification


class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'content', 'timestamp', 'is_read']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = str(data['user'])
        return data
