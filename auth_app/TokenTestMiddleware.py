from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import jwt
from auth_app.models import UserAccount
from django.contrib.auth import settings

class TokenTestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.headers.get('Authorization')
        response = self.get_response(request)
        if authorization_header and authorization_header.startswith('Bearer'):
            access_token = authorization_header.split(":")[1]
            try:
                print('verify',access_token)
                token = AccessToken(access_token)
                token.verify()
            except:
                try:
                    user = UserAccount.objects.filter(access_token = str(access_token)).first()
                    print('user',user)
                    refresh_token = user.refresh_token
                    print(refresh_token)
                    token = RefreshToken(refresh_token)
                    token.verify()
                    access_token = str(token.access_token)
                    user.access_token = access_token
                    user.save()
                    response['Authorization'] = f'Bearer {access_token}'
                except:
                    print('error occured')
        return response








