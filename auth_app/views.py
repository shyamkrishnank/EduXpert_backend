from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserAcoountSerializers, LoginSerializers, InstructorSerializer
from course.serializers import CourseEssentialSerializer

from .models import UserAccount
from .mail import send_otp_via_email
from course.models import Course


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
    serializer_class = LoginSerializers
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)


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
        data = request.data
        try:
            user = UserAccount.objects.get(email=data['email'])
            user_token = user.token()
            return Response({
                'access_token': str(user_token.get('access')),
                'refresh_token': str(user_token.get('refresh')),
                'is_staff': user.is_staff
            })

        except:
            user = UserAccount(first_name=data['given_name'], last_name=data['family_name'], email=data["email"])
            user.save()
            user_token = user.token()
            return Response({
                'access_token': str(user_token.get('access')),
                'refresh_token': str(user_token.get('refresh')),
                'is_staff': user.is_staff
            })




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
