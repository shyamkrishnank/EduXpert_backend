from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import requests
from notification.models import NotificationRoom
import json



from .serializers import UserAcoountSerializers, LoginSerializers, InstructorSerializer

from .models import UserAccount
from .mail import send_otp_via_email


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        cache_data = UserAccount.objects.filter(email=data['email']).first()
        if cache_data:
            if cache_data.is_verified == False:
                cache_data.delete()
            else:
                return Response({'message' : 'Email allready in use!'}, status=status.HTTP_409_CONFLICT)
        otp = send_otp_via_email(data['email'])
        print(otp)
        data['otp'] = otp
        serializer = UserAcoountSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        data = request.data
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise AuthenticationFailed("User not found")
        user_token = user.token()
        data = {
            'access_token': str(user_token.get('access')),
            'is_staff' : user.is_staff,
        }
        room = NotificationRoom.objects.filter(name=f'notifications_{str(user.id)}').first()
        if not room:
            notificationRoom = NotificationRoom(name=f'notifications_{str(user.id)}')
            notificationRoom.save()
        response = Response(data, headers={
            'refresh_token': str(user_token.get('refresh')),
            'Access-Control-Expose-Headers': 'refresh_token'
        })
        return response



class OtpView(APIView):
    permission_classes = []

    def post(self, request):
        otp = request.data['otp']
        email = request.data['email']
        try:
            user = UserAccount.objects.get(email=email)
            if user.otp == otp:
                user.is_verified = True
                user.save()
                serializer = UserAcoountSerializers(user)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"message": 'otp enterd wrong'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"message": "something went wrong"},status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class GoogleLoginView(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data['token']
        GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
        try:
           google_response = requests.get(GOOGLE_ID_TOKEN_INFO_URL, headers={'Authorization': f'Bearer {token}'})
           data = google_response.json()
           if data:
               try:
                   user = UserAccount.objects.get(email=data['email'])
                   user_token = user.token()
                   data = {
                       'access_token': str(user_token.get('access')),
                       'is_staff': user.is_staff,
                       'already_user': True

                   }
                   room = NotificationRoom.objects.filter(name=f'notifications_{str(user.id)}').first()
                   if not room:
                       notificationRoom = NotificationRoom(name=f'notifications_{str(user.id)}')
                       notificationRoom.save()
                   response = Response(data, headers={
                       'refresh_token': str(user_token.get('refresh')),
                       'Access-Control-Expose-Headers': 'refresh_token',

                   })
                   return response
               except:
                    user = UserAccount(first_name=data['given_name'], last_name=data['family_name'], email=data["email"])
                    user.save()
                    user_token = user.token()
                    data = {
                        'access_token': str(user_token.get('access')),
                        'is_staff': user.is_staff,
                    }
                    room = NotificationRoom.objects.filter(name=f'notifications_{str(user.id)}').first()
                    if not room:
                        notificationRoom = NotificationRoom(name=f'notifications_{str(user.id)}')
                        notificationRoom.save()
                    response = Response(data, headers={
                        'refresh_token': str(user_token.get('refresh')),
                        'Access-Control-Expose-Headers': 'refresh_token'
                    })
                    return response
        except Exception as e:
            return Response({'message': 'Sorry Something Went Wrong..!'},status.HTTP_406_NOT_ACCEPTABLE)


class GoogleSignUpView(GoogleLoginView,APIView):

    def post(self,request,is_staff=None):
        response = super().post(request)
        try:
            if response.data['already_user']:
                return Response({'message': 'Already have an account'})
        except:
            return response

    def get(self,request,is_staff,user_id):
        if is_staff.lower() == 'true':
            user = UserAccount.objects.get(id = user_id)
            user.is_staff = True
            user.save()
            print('user saved')
            return Response({'is_staff':True},status=status.HTTP_200_OK)
        return Response({'is_staff',False}, status=status.HTTP_200_OK)



class UserDetailsView(APIView):
    def get(self, request, id):
        print('hello')
        print('user',request.user)
        try:
            user = UserAccount.objects.get(id=id)
            serializer = UserAcoountSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        data = request.data
        user = UserAccount.objects.get(id=id)
        serializer = UserAcoountSerializers(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)

class InstructorProfileView(APIView):

    def get(self,request,id):
        print('hellooo')
        try:
            user = UserAccount.objects.get(id=id)
            serializer = InstructorSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_406_NOT_ACCEPTABLE)
