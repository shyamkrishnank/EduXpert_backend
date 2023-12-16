from django.db import models
from auth_app.models import UserAccount


class CourseCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_description = models.TextField()

    def __str__(self):
        return self.category_name

status = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Cancelled', 'Cancelled')
]

class Course(models.Model):
    course_title = models.CharField(max_length=30)
    course_description = models.TextField(default="no description available!")
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0.00)
    image = models.ImageField(upload_to="course/", null=True, blank=True)
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=status, default='Pending')

    def chapter_count(self):
        chapters = self.chapters.count()
        return chapters


    def __str__(self):
        return self.course_title


class CourseChapter(models.Model):
    title = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=200,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='chapters')
    chapter_no = models.IntegerField(null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='chapterVideo/')
