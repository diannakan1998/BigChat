from django.shortcuts import render

# Create your views here.
import requests
import json


from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core import serializers

from auth.models import Users
from .models import chatModel


def index(request):
     return HttpResponse("chat POST")


# class ChatList(View):
    
#     def get(self, requests):
#          return HttpResponse("ChatList GET")

#     def post(self, requests):
#          return HttpResponse("ChatList POST")


class MessageHistory(View):

    def get(self, requests):
        chatId = requests.GET.get('chatId')
        token = requests.GET.get('token')
        try: 
            user = Users.objects.get(token=token)
            if chatId in user.chat_list_id:
                chat = chatModel(chatId)
                return serializers.serialize('json', chat.objects.raw('select * from public.\"%s\" order by date_added ASC', [chatId]))
            else:
                return JsonResponse({'error' : 'no chat error'})
        except Exception:
            return JsonResponse({'error' : 'chat error'})

    def post(self, requests):
        message = requests.GET.get('message')
        token = requests.GET.get('token')
        chatId = requests.GET.get('chatId')
        messageType = requests.GET.get('type')
        email = requests.GET.get('email')
        try: 
            user = Users.objects.get(token=token)
            if chatId in user.chat_list_id:
                chat = chatModel(chatId)
                chat.objects.raw('insert into public.\"%s\"" (user_email, message, message_type, date_added, date_modified) VALUES(%s, %s, %d, NOW(), NOW())', [chatId], [email], [message], [messageType])
                return JsonResponse({'success' : 'no error'})
            else:
                return JsonResponse({'error' : 'no chat error'})
        except Exception:
            return JsonResponse({'error' : 'chat error'})


