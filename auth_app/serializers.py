from rest_framework import serializers
from .models import UserAccount
from course.models import Course
from course.serializers import CourseEssentialSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate



class UserAcoountSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["id", "first_name", 'last_name','headline','is_active','is_staff','created_at','otp',
                  'image', 'email', 'password','experience', 'phone', 'bio', 'sociallink','otp_expiry']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class LoginSerializers(serializers.ModelSerializer):
    email = serializers.CharField(max_length=200, write_only=True)
    password = serializers.CharField(max_length=200, write_only=True)
    access_token = serializers.CharField(max_length=300, read_only=True)
    refresh_token = serializers.CharField(max_length=300, read_only=True)

    class Meta:
        model = UserAccount
        fields = ['email', 'password', 'is_staff','access_token','refresh_token']

    def validate(self, attrs=None):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("User not found")


        user_token = user.token()

        return {
            'access_token': str(user_token.get('access')),
            'refresh_token': str(user_token.get('refresh')),
            'is_staff' : user.is_staff
        }

class InstructorSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta:
        model = UserAccount
        fields = ["id", 'headline','created_at', 'image', 'email','bio','get_full_name', "course",'sociallink']

    def get_course(self,obj):
        course = Course.objects.filter(created_by=obj.id, is_active=True)
        serializer = CourseEssentialSerializer(course, many=True)
        return serializer.data



class ChatUsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'get_full_name', 'image']