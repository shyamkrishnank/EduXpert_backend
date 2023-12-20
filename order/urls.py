from django.urls import path
from .views import *

urlpatterns = [
    path("razorpay", OrderDetailsView.as_view()),
    path("save", OrderSaveView.as_view()),
    path('user/<int:id>', GetUserOrder.as_view()),
]