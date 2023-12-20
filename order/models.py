from django.db import models
from auth_app.models import UserAccount
from course.models import Course

class Order(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    payment_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    signature = models.CharField(max_length=200)
    status = models.BooleanField(default=True)