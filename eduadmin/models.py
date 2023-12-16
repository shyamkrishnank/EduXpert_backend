from django.db import models
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class EduAdmin(models.Model):
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access_token': str(refresh.access_token),
            'id':self.id
        }
