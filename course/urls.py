from django.urls import path
from .views import *

urlpatterns = [
    path('course_category', CourseCategoryViews.as_view()),
    path('upload_course', CourseUploadViews.as_view()),
    path('get_course/<int:id>', GetCourseDetail.as_view()),
    path('chapter_upload', ChapterUploadView.as_view()),
    path('delete_course/<int:id>', DeleteCourseView.as_view()),
    path('ins_course/<int:id>', GetInstructorCourseView.as_view()),
    path('edit_course/<int:id>', CourseEditView.as_view()),
    path('ins_chapter/<int:id>', GetChapterDetails.as_view()),
    path('course_view/<int:id>', UserCourseView.as_view()),
    path('chapter_details/<int:id>', GetChapterInChaptersView.as_view()),
    path('add_chapter', ChapterAddNewView.as_view()),
    path('userhome', GetUserHomeCourseView.as_view()),
]