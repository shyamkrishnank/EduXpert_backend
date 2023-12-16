from rest_framework.views import APIView
from .models import *
from course.models import Course
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView



class AdminLogin(APIView):
    def post(self, request):
        data = request.data
        try:
            admin = EduAdmin.objects.get(email=data['email'])
            if check_password(data['password'], admin.password):
               token=admin.token()
               token['is_admin'] = True
               print(token)
               return Response(token ,status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Password Entered is Wrong.!'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message': 'No Admin Found.!'}, status=status.HTTP_404_NOT_FOUND)

class SetPage(PageNumberPagination):
    page_size = 2

class CourseView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = SetPage


class CourseDetailedView(APIView):
    def get(self,request, id):
        queryset = Course.objects.get(id = id)
        serializer_class = CourseSerializer(queryset)
        return Response(serializer_class.data)

class CourseActivation(APIView):
    def get(self,request,id):
        course = Course.objects.get(id = id)
        course.is_active = not course.is_active
        if course.is_active:
            course.status = 'Approved'
        else:
            course.status ='Cancelled'
        course.save()
        return Response({'status':course.is_active},status=status.HTTP_200_OK)

class UsersView(ListAPIView):
    queryset = UserAccount.objects.filter(is_staff=False)
    serializer_class = UserAcoountSerializers
    pagination_class = SetPage


class UserDetailView(APIView):
    def get(self,request,id):
        queryset = UserAccount.objects.get(id = id)
        serializer = UserAcoountSerializers(queryset)
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserActivation(APIView):
    def get(self, request, id):
        user = UserAccount.objects.get(id = id)
        user.is_active = not user.is_active
        user.save()
        return Response({'status':user.is_active}, status=status.HTTP_200_OK)

class InstructorsView(ListAPIView):
    queryset = UserAccount.objects.filter(is_staff=True, is_superuser=False)
    serializer_class = UserAcoountSerializers
    pagination_class = SetPage



