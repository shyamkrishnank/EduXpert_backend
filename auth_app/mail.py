from django.core.mail import send_mail
import random
from django.conf import settings


def send_otp_via_email(email):
    subject = "Your account verification email"
    otp = random.randint(1000,9999)
    message = f'{otp} is your OTP for the verification for email for the EduXpert,OTP is confidential and valid for 1 mins'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email], fail_silently=False,)
    return otp