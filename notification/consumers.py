from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import NotificationRoom, Notification
from auth_app.models import UserAccount
import json
from .serializers import NotificationSerializers
from channels.layers import get_channel_layer



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        user_id = str(user)
        self.room_group_name = f'notifications_{user_id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, byte_data=None):
            print(text_data)
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            room = await database_sync_to_async(NotificationRoom.objects.get)(name=self.room_group_name)
            notification = Notification(
                content=message,
                user=await database_sync_to_async(UserAccount.objects.get)(id=self.scope['user']),
                room=room
            )
            await database_sync_to_async(notification.save)()
            data = NotificationSerializers(notification)
            await  self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': data.data
                }
            )

    async def notification_message(self, event):
        print('notification',event)
        message = event['message']
        await self.send(text_data=json.dumps(message))




# sending notification
async def send_notification_to_user(user_channel_name, message,user_id):
    channel_layer = get_channel_layer()
    room = await database_sync_to_async(NotificationRoom.objects.get)(name=user_channel_name)
    notification = Notification(
        content=message,
        user=await database_sync_to_async(UserAccount.objects.get)(id=user_id),
        room=room
    )
    await database_sync_to_async(notification.save)()
    data = NotificationSerializers(notification)
    await channel_layer.group_send(
        user_channel_name,
        {
            'type': 'notification_message',
            'message': data.data,
        }
    )

