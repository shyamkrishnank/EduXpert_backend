from django.db import models
from auth_app.models import UserAccount
from course.models import Course
import uuid

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    payment_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    signature = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='wallet')
    amount = models.FloatField(default=0.0)