from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=300,null=True)
    headline = models.CharField(max_length=300, null=True)
    bio = models.TextField(null=True)
    sociallink = models.TextField(null=True)
    image = models.ImageField(upload_to='users',null=True)
    email = models.CharField(max_length=300,unique=True)
    otp = models.CharField(max_length=10, null=True)
    is_verified = models.BooleanField(default=False)
    is_googleAuth = models.BooleanField(default=False)
    experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    refresh_token = models.CharField(default=None,null=True, max_length=300)
    access_token = models.CharField(default=None,null=True, max_length=300)
    username = None

    object = CustomUserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_short_name(self):
        return f'{self.first_name}'

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

