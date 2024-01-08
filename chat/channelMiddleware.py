from channels.middleware import BaseMiddleware
from django.db import close_old_connections
import jwt
from django.contrib.auth import settings
from uuid import UUID



class JWTwebsocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()
        print(scope)
        query_string = scope.get('query_string', b"").decode('utf-8','replace')
        print(query_string)
        try:
            query_params = dict(qp.split('=') for qp in query_string.split('&'))
        except:
            query_params = dict(query_string.split("="))
        token = query_params.get('token', None)
        recever_id = query_params.get('chat_with', None)
        if token is None:
            await send({
                'type': 'websocket.close',
                'code': 4000
            })
        else:
           id = jwt.decode(token ,settings.SECRET_KEY, algorithms=['HS256'],options={'verify_exp': False})['user_id']
           user_id = UUID(id)
           try:
               try:
                   user = user_id
                   chat_with = recever_id
               except Exception as e:
                   print('no user found', e)
               if user:
                   scope['user'] = user
                   scope['chat_with'] = chat_with
               else:
                   await send({
                       'type': 'websocket.close',
                       'code': 4000
                   })
               return await super().__call__(scope, receive, send)
           except Exception as e:
                print(e)


