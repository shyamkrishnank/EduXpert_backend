from django.urls import path
from .views import *

urlpatterns = [
    path('course_category', CourseCategoryViews.as_view()),
    path('upload_course', CourseUploadViews.as_view()),
    path('get_course/<uuid:id>', GetCourseDetail.as_view()),
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

]