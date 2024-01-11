from rest_framework import serializers
from .models import Order,Wallet
from auth_app.models import UserAccount
from course.models import Course

class OrderConfirmedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class GetUserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = ['id']

class OrderUserDetails(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'get_full_name']

class OrderCourseDetails(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_title']

class InstructorOrderSerializer(serializers.ModelSerializer):
    user = OrderUserDetails(read_only=True)
    course = OrderCourseDetails(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'


#full order details serializers
class UserDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id','get_full_name','email', 'phone', 'image']

class CourseDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course_title','price','image','chapter_count','status']

class OrderFullDetailsSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializers(read_only=True)
    course = CourseDetailsSerializers(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class WalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'