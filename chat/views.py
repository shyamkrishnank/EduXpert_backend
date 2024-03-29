from django.shortcuts import render
from auth_app.models import UserAccount
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import settings
import jwt
import uuid
from .serializers import ChatSerializer
from auth_app.serializers import ChatUsersSerializers
from notification.models import NotificationRoom, Notification
from .models import Chat, ChatRoom


class Chats(APIView):
    def get(self, request, id):
        all_chats = []
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer'):
            access_token = authorization_header.split(" ")[1]
            try:
                user_id = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'], options={'verify_exp': False})['user_id']
            except Exception as e:
                print(e)
            user_ids = [str(user_id), str(id)]
            user_ids = sorted(user_ids)
            room_group_name = f'chat_{user_ids[0]}_{user_ids[1]}'
            room = NotificationRoom.objects.get(name=f'notifications_{user_id}')
            notification = Notification.objects.filter(room=room, user=UserAccount.objects.get(id=id), is_read=False)
            if notification:
                for obj in notification:
                    obj.is_read = True
                    obj.save()
            room = ChatRoom.objects.filter(name=room_group_name).first()
            if room:
                chats = Chat.objects.filter(room = room)
                if chats:
                   all_chats = ChatSerializer(chats, many=True)
                   return Response(all_chats.data, status=status.HTTP_200_OK)
            else:
                create_room = ChatRoom(name = room_group_name)
                create_room.save()
        return Response(all_chats, status.HTTP_200_OK)


class ChatLists(APIView):
    def get(self,request,id):
        chatroom = ChatRoom.objects.filter(name__contains=str(id))
        users = []
        if chatroom:
            for room in chatroom:
                ids = room.name.split('_')
                ids.pop(0)
                ids = [i for i in ids if i != str(id)]
                print('ids',ids)
                if ids:
                   users.append(UserAccount.objects.get(id = uuid.UUID(ids[0])))
            if users:
                users_serializer = ChatUsersSerializers(users, many=True)
                return Response(users_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response([],status=status.HTTP_200_OK)
        return Response(users,status=status.HTTP_200_OK)










