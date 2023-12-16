from rest_framework import serializers
from course.models import Course, CourseChapter
from auth_app.models import UserAccount


class Created_bySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'first_name']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    created_by =  Created_bySerializer(many=False, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

class InstructorsCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_title']


class UserAcoountSerializers(serializers.ModelSerializer):
    courses = InstructorsCourseSerializer(many=True, read_only=True)
    class Meta:
        model = UserAccount
        fields = ["id", "first_name", 'last_name','headline','is_active','is_staff','created_at',
                  'image', 'email', 'courses', 'phone', 'bio', 'sociallink']
