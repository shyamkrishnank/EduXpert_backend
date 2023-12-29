from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import requests



from .serializers import UserAcoountSerializers, LoginSerializers, InstructorSerializer

from .models import UserAccount
from .mail import send_otp_via_email


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        cache_data = UserAccount.objects.filter(email=data['email'], is_verified=False)
        if cache_data.exists():
            cache_data.delete()
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
    def post(self, request):
        data = request.data
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise AuthenticationFailed("User not found")
        user_token = user.token()
        user.refresh_token = str(user_token.get('refresh'))
        user.access_token = str(user_token.get('access'))
        user.save()
        data = {
            'access_token': user.access_token,
            'is_staff' : user.is_staff
        }
        return Response(data)



class OtpView(APIView):
    def post(self, request):
        otp = request.data['otp']
        email = request.data['email']
        try:
            user = UserAccount.objects.get(email=email)
            if user.otp == otp:
                user.is_verified = True
                user.save()
                return Response({"message": 'success'})
            else:
                return Response({"message": 'otp enterd wrong'})
        except:
            return Response({"message": "something went wrong"})

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data
        GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
        try:
           google_response = requests.get(GOOGLE_ID_TOKEN_INFO_URL, headers={'Authorization': f'Bearer {token}'})
           data = google_response.json()
           if data:
               try:
                   user = UserAccount.objects.get(email=data['email'])
                   user_token = user.token()
                   user.refresh_token = str(user_token.get('refresh'))
                   user.access_token = str(user_token.get('access'))
                   user.save()
                   return Response({
                        'access_token': user.access_token,
                        'is_staff': user.is_staff
                    })
               except:
                    user = UserAccount(first_name=data['given_name'], last_name=data['family_name'], email=data["email"])
                    user_token = user.token()
                    user.refresh_token = str(user_token.get('refresh'))
                    user.access_token = str(user_token.get('access'))
                    user.save()
                    return Response({
                        'access_token': user.access_token,
                        'is_staff': user.is_staff
                    })
        except:
            return Response({'message':'Sorry Something Went Wrong..!'},status.HTTP_406_NOT_ACCEPTABLE)








class UserDetailsView(APIView):
    def get(self, request, id):
        try:
            user = UserAccount.objects.get(id=id)
            serializer = UserAcoountSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        data = request.data
        print(data)
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
        try:
            user = UserAccount.objects.get(id=id)
            serializer = InstructorSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "user not found"}, status=status.HTTP_406_NOT_ACCEPTABLE)
