from django.urls import path
from .views import *

urlpatterns = [
    path("razorpay", OrderDetailsView.as_view()),
    path("save", OrderSaveView.as_view()),
    path('user/<uuid:id>', GetUserOrder.as_view()),
]