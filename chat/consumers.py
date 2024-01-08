from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .models import ChatRoom, Chat
from auth_app.models import UserAccount
from .serializers import ChatSerializer
from notification.consumers import send_notification_to_user



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_user = self.scope['user']
        chat_with_user = self.scope['chat_with']
        user_ids = [str(request_user), str(chat_with_user)]
        user_ids = sorted(user_ids)
        self.room_group_name = f'chat_{user_ids[0]}_{user_ids[1]}'
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room = await database_sync_to_async(ChatRoom.objects.get)(name = self.room_group_name)
        chat = Chat(
            content=message,
            user=await database_sync_to_async(UserAccount.objects.get)(id = self.scope['user']),
            room=room
        )
        await database_sync_to_async(chat.save)()
        data = ChatSerializer(chat)
        await  self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data.data
            }
        )
        await send_notification_to_user(f'notifications_{str(self.scope["chat_with"])}','You have a message',str(self.scope['user']))
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
