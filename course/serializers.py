from rest_framework import serializers
from .models import Course, CourseChapter, CourseCategory
from auth_app.models import UserAccount

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'category_name']

class CourseNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = ['id','course_title']

class ChapterForEditSerializer(serializers.ModelSerializer):
    course = CourseNameSerializer(read_only=True)
    class Meta:
        model = CourseChapter
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = '__all__'

class CreatedByUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'get_full_name']

class ChapterNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseChapter
        fields = ['id', 'title', 'description']

class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterNamesSerializer(many=True, read_only=True)
    course_category = CategoryNameSerializer(read_only=True)
    created_by = CreatedByUserNameSerializer(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'



class CourseEssentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course_title','image',]





