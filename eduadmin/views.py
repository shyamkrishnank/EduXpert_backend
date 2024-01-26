from rest_framework.views import APIView
from .models import *
from order.models import *
from order.serializers import InstructorOrderSerializer
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from course.serializers import CourseSearchSerializers

from datetime import timedelta
from django.utils import timezone







class AdminLogin(APIView):
    def post(self, request):
        data = request.data
        try:
            user = authenticate(email=data['email'], password=data['password'])
            if user:
               print(user)
               if user.is_superuser:
                   token=user.token()
                   logged_data = {}
                   logged_data['is_admin'] = True
                   logged_data['access_token'] = token['access']
                   print(logged_data)
                   response = Response(logged_data, headers={
                       'refresh_token': str(token.get('refresh')),
                       'Access-Control-Expose-Headers': 'refresh_token'
                   })
                   return response
               else:
                   Response({'message':'Not an admin!'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'Password Entered is Wrong.!'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message': 'No Admin Found.!'}, status=status.HTTP_404_NOT_FOUND)

class SetPage(PageNumberPagination):
    page_size = 6

class CourseView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = SetPage


class CourseDetailedView(APIView):
    def get(self,request, id):
        queryset = Course.objects.get(id = id)
        serializer_class = CourseSerializer(queryset)
        return Response(serializer_class.data)

class SetPageOnChapter(PageNumberPagination):
    page_size = 1

class ChapterView(ListAPIView):
    serializer_class = ChapterSerializer
    pagination_class = SetPageOnChapter
    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if course_id is not None:
            try:
                return CourseChapter.objects.filter(course__id=course_id)
            except ValueError:
                return CourseChapter.objects.none()
        else:
            return None


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


class AdminDashboard(APIView):
    def get(self,request):
        seven_days_ago = timezone.now() - timedelta(days=6)
        date_list = [seven_days_ago + timedelta(days=i) for i in range(7)]
        result_data = {'date':[],'order_count':[],'user_count':[],'instructor_count':[]}
        for date in date_list:
            order_count = Order.objects.filter(ordered_at__date=date).count()
            user_count = UserAccount.objects.filter(is_staff = False,created_at__date = date).count()
            instructor_count = UserAccount.objects.filter(is_staff = True,is_superuser = False,created_at__date = date).count()
            formated_date = date.strftime('%d/%m/%Y')
            result_data['date'].append(formated_date)
            result_data['order_count'].append(order_count)
            result_data['user_count'].append(user_count)
            result_data['instructor_count'].append(instructor_count)
        result_data['total_instructor_count'] = UserAccount.objects.filter(is_staff = True, is_superuser = False).count()
        result_data['total_user_count'] = UserAccount.objects.filter(is_staff = False).count()
        result_data['total_course_count'] = Course.objects.filter(is_active = True).count()
        pending_courses = Course.objects.filter(status = "Pending")
        if pending_courses:
             serializer = CourseSearchSerializers(pending_courses, many=True)
             result_data['pending_courses']  = serializer.data
        else:
            result_data['pending_courses'] = None
        print(result_data)
        return Response(result_data,status=status.HTTP_200_OK)

class Orders(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = InstructorOrderSerializer
    pagination_class = SetPage






