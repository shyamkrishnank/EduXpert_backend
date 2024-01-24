from django.urls import path
from .views import *

urlpatterns = [
    path('course_category', CourseCategoryViews.as_view()),
    path('upload_course', CourseUploadViews.as_view()),
    path('get_course/<uuid:id>', GetCourseDetail.as_view()),
    path('get_allcourse/', GetAllCourses.as_view()),
    path('search_course/<str:character>',CourseSearchView.as_view()),
    path('search_course/',CourseSearchView.as_view()),
    path('chapter_upload', ChapterUploadView.as_view()),
    path('delete_course/<uuid:id>', DeleteCourseView.as_view()),
    path('ins_course/<uuid:id>', GetInstructorCourseView.as_view()),
    path('edit_course/<uuid:id>', CourseEditView.as_view()),
    path('edit_chapter/<uuid:id>', ChapterEditView.as_view()),
    path('ins_chapter/<uuid:id>', GetChapterDetails.as_view()),
    path('course_view/<uuid:id>', UserCourseView.as_view()),
    path('chapter_details/<uuid:id>', GetChapterInChaptersView.as_view()),
    path('add_chapter', ChapterAddNewView.as_view()),
    path('userhome', GetUserHomeCourseView.as_view()),

    path('addreview/', AddReview.as_view()),
    path('get_review/<uuid:course_id>', GetAllReview.as_view()),
    path('like_review/<uuid:review_id>', LikedReview.as_view()),
    path('delete_review/<uuid:review_id>', DeleteReview.as_view()),

    path('instructor_review/<uuid:instructor_id>', InstructorReview.as_view()),
    path('review_reply/', InstructorReply.as_view()),
    path('delete_reply/<uuid:reply_id>', DeleteReply.as_view()),

]