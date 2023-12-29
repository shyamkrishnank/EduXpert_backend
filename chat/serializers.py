from rest_framework import serializers
from .models import Chat, ChatRoom
from auth_app.models import UserAccount




class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['content','timestamp','user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = str(data['user'])
        return data


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

