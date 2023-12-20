from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class TokenTestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.headers.get('Authorization')
        response = self.get_response(request)
        if authorization_header and authorization_header.startswith('Bearer'):
            Bearer = authorization_header.split(" ")[0]
            access_token = Bearer.split(":")[1]
            try:
                token = AccessToken(access_token)
                token.verify()
            except:
                Bearer = authorization_header.split(" ")[1]
                refresh_token = Bearer.split(":")[1]
                try:
                    token = RefreshToken(refresh_token)
                    token.verify()
                    access_token = str(token.access_token)
                    print("ith puthiyeee access aa",access_token)
                    response['Authorization'] = f'Bearer {access_token}'
                    print(response.headers)
                except:
                    pass
        return response








