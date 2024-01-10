from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from razorpay import Client
from django.conf import settings
from rest_framework.pagination import PageNumberPagination



from auth_app.models import UserAccount
from .models import Order
from .serializers import *
from course.serializers import CourseEssentialSerializer


class OrderDetailsView(APIView):
    def post(self, request):
        data = request.data
        order_data = {"amount": data['amount']*100, "currency": "INR", "receipt": "order_rcptid_11"}
        client = Client(auth=(settings.RAZOR_KEY,settings.RAZOR_KEY_SECRET))
        payment = client.order.create(data=order_data)
        key_data = {
            "razor_key" : settings.RAZOR_KEY,
            "razor_key_secret" : settings.RAZOR_KEY_SECRET,
            'payment' : payment,
            'id' : data['id']
        }
        return Response(key_data, status=status.HTTP_200_OK)


class OrderSaveView(APIView):
    def post(self,request):
        data = request.data
        serializer = OrderConfirmedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'saved'},status=status.HTTP_200_OK)
        return Response({'message':'not saved'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class GetUserOrder(APIView):
   def get(self,request,id):
       orders=Order.objects.filter(user=UserAccount.objects.get(id=id))
       if orders:
           courses = [order.course for order in orders]
           serializer = CourseEssentialSerializer(courses, many=True)
           return Response(serializer.data,status=status.HTTP_200_OK)
       return Response({'message':'not found'}, status=status.HTTP_404_NOT_FOUND)


#orders in the instructor side
class SetPage(PageNumberPagination):
    page_size = 8

class InstructorCourseOrders(generics.ListAPIView):
    serializer_class = InstructorOrderSerializer
    pagination_class = SetPage


    def get_queryset(self):
        instructor_id = self.kwargs['instructor_id']
        return Order.objects.filter(course__created_by__id = instructor_id)


class OrderDetailsView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderFullDetailsSerializer
    lookup_field = 'id'






