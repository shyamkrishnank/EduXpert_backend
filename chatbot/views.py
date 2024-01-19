from django.shortcuts import render
from openai import  OpenAI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class Chatbot(APIView):
    def post(self,request):
        data = request.data
        print(data)
        try:
            client = OpenAI(
                api_key=settings.OPENAI_KEY
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {'role': 'user', 'content': f'{data["message"]}. Answer in three sentence or less'}
                ],
                model='gpt-3.5-turbo',
            )
            print(chat_completion.choices[0].message.content)
            return Response({'message':chat_completion.choices[0].message.content},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message':"Sorry I am not Able to Answer Right Now"},status=status.HTTP_200_OK)


