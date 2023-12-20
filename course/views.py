from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from order.models import Order

class CourseCategoryViews(APIView):
    def get(self, request):
        course = CourseCategory.objects.values('id', 'category_name')
        data = dict()
        for i in course:
            data[i['category_name']] = i['id']
        return Response({"data": data})


class GetChapterDetails(APIView):
    def get(self, request, id):
        course = Course.objects.get(id = id)
        chapters = CourseChapter.objects.filter(course = course)
        if chapters:
            initial_chapter = chapters.first()
            intial_chapter_serializer = ChapterSerializer(initial_chapter)
            all_chapter_serializer = ChapterNamesSerializer(chapters, many=True)
            data = {
                'initial_chapter': intial_chapter_serializer.data,
                'all_chapters': all_chapter_serializer.data,
                'instructor' : {
                    'id':course.created_by.id,
                    'get_full_name':course.created_by.get_full_name,

                }
            }
        else:
            data = {
                'intial_chapter':None,
                'all_chapters' : None
            }
        return Response(data, status=status.HTTP_200_OK)


class GetCourseDetail(GetChapterDetails, APIView):
    def get(self, request, id):
        course = Course.objects.get(id=id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def post(self,request,id):
        course = Course.objects.get(id=id)
        if course.is_active:
            user_id = request.data['user_id']
            if Order.objects.filter(user=UserAccount.objects.get(id=user_id),course=course).exists():
                response = super().get(request, id)
                response.data['message']='purchased'
                print(response.data)
                return Response(response.data,status=status.HTTP_200_OK)
            serializer = CourseSerializer(course)
            response = serializer.data
            response['message']='not purchased'
            return Response(response)
        return Response({'message':'Sorry Course is not Available'},status=status.HTTP_404_NOT_FOUND)



class GetChapterInChaptersView(APIView):
    def get(self, request, id):
        chapter = CourseChapter.objects.get(id = id)
        intial_chapter_serializer = ChapterSerializer(chapter)
        all_chapters = CourseChapter.objects.filter(course = chapter.course)
        instructor =UserAccount.objects.get(id=chapter.course.created_by.id)
        if all_chapters:
            all_chapter_serializer = ChapterNamesSerializer(all_chapters, many=True)
            data = {
                'initial_chapter': intial_chapter_serializer.data,
                'all_chapters': all_chapter_serializer.data,
                'instructor': {
                    'id': chapter.course.created_by.id,
                    'get_full_name': chapter.course.created_by.get_full_name,
                }
            }
        else:
            data = {
                'initial_chapter': intial_chapter_serializer.data,
                'all_chapters': None
            }
        return  Response(data, status=status.HTTP_200_OK )






class GetInstructorCourseView(APIView):
    def get(self,request,id):
        course = Course.objects.filter(created_by=(UserAccount.objects.get(id=id)))
        if course:
            serializer = CourseSerializer(course,many=True)
            return Response(serializer.data,status.HTTP_200_OK)
        else:
            return Response({'message':'no course'},status.HTTP_404_NOT_FOUND)





class CourseUploadViews(APIView):
    def post(self, request):
        data = {
            'course_title': request.data.get('course_title'),
            'course_description': request.data.get('course_description'),
            'course_category': int(request.data.get("course_category")),
            'created_by': int(request.data.get('created_by')),
            'price': float(request.data.get('price')),
            'image': request.data.get('image'),
        }
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChapterUploadView(APIView):
    def post(self, request):
        data = request.data
        numOfChapter = len(data) // 3
        course = Course.objects.get(id = data['course_id'])
        for i in range(0, numOfChapter):
            chapter = {}
            for key, value in data.items():
                if key[-1] == str(i):
                    chapter[key[:-2]] = value
            chapter['course']=int(data['course_id'])
            chapter['chapter_no'] = Course.chapter_count(course) + 1
            serializer = ChapterSerializer(data=chapter)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'message': ''}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message':'completed'}, status=status.HTTP_200_OK)

class ChapterAddNewView(GetChapterDetails, APIView):
    def post(self,request):
        data = request.data
        id = data['course_id']
        course = Course.objects.get(id=data['course_id'])
        data['course'] = int(data['course_id'])
        data['chapter_no'] = Course.chapter_count(course) + 1
        serializer = ChapterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            chapters = self.get(request, id)
            return Response(chapters.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': ''}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(chapters.data)
        return Response({'message': ''}, status=status.HTTP_200_OK)


class CourseEditView(APIView):
    def post(self,request,id):
        data = request.data
        course = Course.objects.get(id=id)
        serializer = CourseSerializer(course, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
class DeleteCourseView(APIView):
    def get(self,request,id):
        course = Course.objects.get(id = id)
        course.delete()
        return Response({'message':'deleted'},status=status.HTTP_200_OK)

#     user page course rendenring...........

class UserCourseView(APIView):
    def get(self, request, id):
        category = CourseCategory.objects.get(id = id)
        course = Course.objects.filter(course_category = category,is_active = True)
        serializer = CourseEssentialSerializer(course, many=True)
        data = {
            'course' : serializer.data,
            'category' : category.category_name
        }
        return Response(data, status=status.HTTP_200_OK)

class GetUserHomeCourseView(APIView):
    def get(self,request):
        course = Course.objects.filter(is_active=True).order_by('?')[:3]
        serializer = CourseEssentialSerializer(course, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)






