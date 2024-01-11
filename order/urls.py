from django.urls import path
from .views import *

urlpatterns = [
    path("razorpay", OrderRazorView.as_view()),
    path("save", OrderSaveView.as_view()),
    path('user/<uuid:id>', GetUserOrder.as_view()),
    path('instructor/<uuid:instructor_id>', InstructorCourseOrders.as_view()),
    path('orderdetailview/<uuid:id>', OrderDetailsView.as_view()),
    path('instructor_wallet/<uuid:id>', InstructorWallet.as_view() )

]