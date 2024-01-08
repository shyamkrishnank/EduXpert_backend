from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NotificationRoom,Notification
from .serializers import NotificationSerializers
from auth_app.models import UserAccount



class Notifications(APIView):
    def get(self,request):
        user = request.user
        id = str(user.id)
        room = NotificationRoom.objects.filter(name = f'notifications_{id}').first()
        if room:
            notifications = Notification.objects.filter(room = room,is_read = False)
            if notifications:
                notificationSerializer = NotificationSerializers(notifications, many=True)
                return Response(notificationSerializer.data, status=status.HTTP_200_OK)
            return Response([], status=status.HTTP_200_OK)
        else:
            notificationRoom = NotificationRoom(name = f'notifications_{id}')
            notificationRoom.save()
            return Response([], status=status.HTTP_200_OK)

class NotificationStatusChange(APIView):
    def get(self,request,id):
        user = request.user
        room = NotificationRoom.objects.get(name = f'notifications_{user.id}')
        notification = Notification.objects.filter(room = room, user = UserAccount.objects.get(id = id), is_read = False)
        if notification:
            for obj in notification:
                obj.is_read = True
                obj.save()
        notifications = Notification.objects.filter(room = room,is_read = False)
        if notifications:
            notificationSerializer = NotificationSerializers(notifications, many=True)
            return Response(notificationSerializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)



