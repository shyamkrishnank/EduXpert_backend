from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from order.models import Order
from rest_framework.authentication import TokenAuthentication


class CourseCategoryViews(APIView):
    permission_classes = []

    def get(self, request):
        course = CourseCategory.objects.values('id', 'category_name')
        data = dict()
        for i in course:
            data[i['category_name']] = i['id']
        return Response({"data": data})


class CourseSearchView(APIView):
    def get(self, request, character=None):
        if character == None:
            return Response(status=status.HTTP_200_OK)
        queryset = Course.objects.filter(course_title__istartswith=character)
        if queryset:
            serializer = CourseSearchSerializers(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class GetChapterDetails(APIView):
    def get(self, request, id):
        course = Course.objects.get(id=id)
        chapters = CourseChapter.objects.filter(course=course)
        if chapters:
            initial_chapter = chapters.first()
            intial_chapter_serializer = ChapterSerializer(initial_chapter)
            all_chapter_serializer = ChapterNamesSerializer(chapters, many=True)
            data = {
                'initial_chapter': intial_chapter_serializer.data,
                'all_chapters': all_chapter_serializer.data,
                'instructor': {
                    'id': course.created_by.id,
                    'get_full_name': course.created_by.get_full_name,

                }
            }
        else:
            data = {
                'intial_chapter': None,
                'all_chapters': None
            }
        return Response(data, status=status.HTTP_200_OK)


class GetCourseDetail(GetChapterDetails, APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, id):
        print(request.user)
        course = Course.objects.get(id=id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def post(self, request, id):
        course = Course.objects.get(id=id)
        if course.price == 0:
            response = super().get(request, id)
            response.data['message'] = 'purchased'
            return Response(response.data, status=status.HTTP_200_OK)
        if course.is_active:
            user_id = request.data['user_id']
            if Order.objects.filter(user=UserAccount.objects.get(id=user_id), course=course).exists():
                response = super().get(request, id)
                response.data['message'] = 'purchased'
                return Response(response.data, status=status.HTTP_200_OK)
            serializer = CourseSerializer(course)
            response = serializer.data
            response['message'] = 'not purchased'
            return Response(response)
        return Response({'message': 'Sorry Course is not Available'}, status=status.HTTP_404_NOT_FOUND)


class GetChapterInChaptersView(APIView):
    def get(self, request, id):
        chapter = CourseChapter.objects.get(id=id)
        intial_chapter_serializer = ChapterSerializer(chapter)
        all_chapters = CourseChapter.objects.filter(course=chapter.course)
        instructor = UserAccount.objects.get(id=chapter.course.created_by.id)
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
        return Response(data, status=status.HTTP_200_OK)


class GetInstructorCourseView(APIView):
    def get(self, request, id):
        print(id)
        course = Course.objects.filter(created_by=(UserAccount.objects.get(id=id)))
        if course:
            serializer = CourseSerializer(course, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'message': 'no course'}, status.HTTP_404_NOT_FOUND)


class CourseUploadViews(APIView):

    def post(self, request):
        print(request.data)
        data = request.data
        serializer = CourseUploadSerializer(data=data)
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
        course = Course.objects.get(id=data['course_id'])
        for i in range(0, numOfChapter):
            chapter = {}
            for key, value in data.items():
                if key[-1] == str(i):
                    chapter[key[:-2]] = value
            chapter['course'] = data['course_id']
            chapter['chapter_no'] = Course.chapter_count(course) + 1
            serializer = ChapterSerializer(data=chapter)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'message': ''}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'completed'}, status=status.HTTP_200_OK)


class ChapterAddNewView(GetChapterDetails, APIView):
    def post(self, request):
        data = request.data
        id = data['course']
        course = Course.objects.get(id=data['course'])
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
    def post(self, request, id):
        data = request.data
        course = Course.objects.get(id=id)
        serializer = CourseSerializer(course, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ChapterEditView(APIView):
    def post(self, request, id):
        data = request.data
        chapter = CourseChapter.objects.get(id=id)
        chapter_serializer = ChapterSerializer(chapter, data=data, partial=True)
        if chapter_serializer.is_valid():
            chapter_serializer.save()
            return Response(chapter_serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Something went wrong'}, status=status.HTTP_200_OK)


class DeleteCourseView(APIView):
    def get(self, request, id):
        course = Course.objects.get(id=id)
        order = Order.objects.filter(course=course)
        if order:
            data = {'message': 'There are purchases for the course, Could not procced the delete request'}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        course.delete()
        return Response({'message': 'deleted'}, status=status.HTTP_200_OK)


#     user page course rendenring...........

class UserCourseView(APIView):
    def get(self, request, id):
        category = CourseCategory.objects.get(id=id)
        course = Course.objects.filter(course_category=category, is_active=True)
        serializer = CourseEssentialSerializer(course, many=True)
        data = {
            'course': serializer.data,
            'category': category.category_name
        }
        return Response(data, status=status.HTTP_200_OK)


class GetUserHomeCourseView(APIView):
    def get(self, request):
        course = Course.objects.filter(is_active=True).order_by('?')[:3]
        serializer = CourseEssentialSerializer(course, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllCourses(APIView):
    permission_classes = []

    def get(self, request):
        category = CourseCategory.objects.all()
        all_course = {}
        for i in category:
            course = Course.objects.filter(course_category=i, is_active=True)
            serializer = CourseEssentialSerializer(course, many=True)
            all_course[i.category_name] = serializer.data
        return Response(all_course, status=status.HTTP_200_OK)


# reviews.....

class AddReview(APIView):
    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = AddReviewSerializer(data=data)
        if serializer.is_valid():
            saved_review = serializer.save()
            serialized_data = GetAllReviewSerializer(saved_review).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Sorry something went wrong'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class GetAllReview(APIView):
    def get(self, request, course_id):
        reviews = Reviews.objects.filter(course=course_id).order_by('-timestamp')
        serializer = GetAllReviewSerializer(reviews, many=True)
        data = serializer.data
        for review in data:
            like_model = ReviewLikes.objects.filter(review=Reviews.objects.get(id=review['id']),
                                                    user=request.user).first()
            if like_model:
                is_liked = like_model.is_liked
            else:
                is_liked = False
            review['is_liked'] = is_liked
        return Response(data, status=status.HTTP_200_OK)


class LikedReview(APIView):
    def get(self, request, review_id):
        review = Reviews.objects.get(id=review_id)
        like_review, created = ReviewLikes.objects.get_or_create(review=review, user=request.user)
        if not created:
            like_review.is_liked = not like_review.is_liked
            like_review.save()
        else:
            like_review.save()
        return Response(status=status.HTTP_200_OK)


class DeleteReview(APIView):
    def get(self, request, review_id):
        review = Reviews.objects.get(id=review_id)
        review.delete()
        return Response(status=status.HTTP_200_OK)

    # instuctor Review

class SetPage(PageNumberPagination):
    page_size = 4

class InstructorReview(ListAPIView):
    queryset = Reviews.objects.all()
    serializer_class = GetInstructorReviewSerializer
    pagination_class = SetPage
    def get_queryset(self):
        instructor_id = self.kwargs['instructor_id']
        return Reviews.objects.filter(course__created_by__id = instructor_id).order_by('-timestamp')


class InstructorReply(APIView):
    def post(self,request):
        data = request.data
        data['user'] = str(request.user.id)
        print(data)
        serializer = ReplySaveSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'message':'Something went wrong!'})
        return Response(serializer.data,status=status.HTTP_200_OK)



class DeleteReply(APIView):
    def get(self,request,reply_id):
        reply = ReviewRepley.objects.get(id = reply_id)
        reply.delete()
        return Response({'message','Reply deleted Successfully'},status=status.HTTP_200_OK)
