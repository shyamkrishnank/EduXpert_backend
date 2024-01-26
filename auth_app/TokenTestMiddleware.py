import time

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status
from rest_framework.response import Response

import jwt
from django.contrib.auth import settings


class TokenTestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def set_response_token(self, response, access_token):
        print('response modified')
        response['access_token'] =str(access_token)
        response['Access-Control-Expose-Headers'] = 'access_token'
        print(response.headers)
        return response

    def __call__(self, request, *args, **kwargs):
        print('middleware Started')
        print(request.headers)
        authorization_header = request.headers.get('Authorization')
        if authorization_header and authorization_header.startswith('Bearer'):
            print('helloo')
            access_token = authorization_header.split(" ")[1]
            print('access initialted ----', access_token)
            try:
                token = AccessToken(access_token)
                token.verify()
                print('token initally verified')
                exp_time = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])['exp']
                if exp_time - time.time() < 600:
                    print('expired time')
                    refresh_token = request.headers['Refresh-Token']
                    print('refresh', refresh_token)
                    token = RefreshToken(refresh_token)
                    token.verify()
                    print('new access created')
                    response = self.get_response(request)
                    modified_res = self.set_response_token(response, token.access_token)
                    return modified_res
                else:
                    print('noooo')
                    print('token verified')
            except:
                try:
                    print('access is invalid ready to set the refresh')
                    refresh_token = request.headers['Refresh-Token']
                    print('refresh',refresh_token)
                    print('old access',access_token)
                    token = RefreshToken(refresh_token)
                    token.verify()
                    print('chek acces',token.access_token)
                    response = self.get_response(request)
                    modified_res = self.set_response_token(response, token.access_token)
                    print('Succededd ------>')
                    return modified_res
                except Exception as e:
                    return Response({'message':'Token Expired Please Login Again'}, status=status.HTTP_401_UNAUTHORIZED)
        response = self.get_response(request)
        return response









