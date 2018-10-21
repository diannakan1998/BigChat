from django.shortcuts import render

# Create your views here.
import requests
import json


from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core import serializers
from django.utils import timezone

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
            print(user.user_id)
            if chatId in user.chat_list_id:
                print(user.chat_list_id)
                chats = chatModel(chatId)
                print(chatId)
                c = chats.objects.all().order_by('date_added')
                listm = getChatListModel("chat_list_"+user.user_id)
                cl.flag = 0
                cl.save()

                jsonObjRoot = { "messages": []}
                for i in c:
                    jsonObj = { "user_email" : 1, "message": 1, "type": 1, "time": 1}
                    jsonObj['user_email'] = i.user_email
                    jsonObj['message'] = i.message
                    jsonObj['type'] = i.message_type
                    jsonObj['time'] = i.date_added.timestamp()
                    jsonObjRoot["messages"].append(jsonObj)
                print(jsonObjRoot)
                return JsonResponse(jsonObjRoot)
            else:
                return JsonResponse({'error' : 'no chat error'})
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chat error'})

    def post(self, requests):
        message = requests.GET.get('message')
        token = requests.GET.get('token')
        chatId = requests.GET.get('chatId')
        mtype = requests.GET.get('type')
        email = requests.GET.get('email')
        print(message)
        try: 
            user = Users.objects.get(token=token)
            if chatId in user.chat_list_id:
                print(user.chat_list_id)
                chat = chatModel(chatId)
                msgn = chat(user_email=email, message=message, message_type=mtype, user_id=user.user_id)
                msgn.save()
                listm = getChatListModel("chat_list_"+user.user_id)
                cl = listm.objects.get(chat_id=chatId)
                cl.date_modified = msgn.date_added
                cl.message = message
                cl.message_type = mtype
                cl.flag = 1
                cl.save()
                return JsonResponse({'success' : 200})
            else:
                return JsonResponse({'error' : 'no chat error'})
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chat error'})


class chatlist(View):

    def get(self, requests):
        token = requests.GET.get('token')
        try:
            user = Users.objects.get(token=token)
            listm = getChatListModel("chat_list_"+user.user_id)
            cl = listm.objects.all().order_by('-date_modified')
            jsonObjRoot = { "chats": []}
            for i in cl:
                jsonObj = { "chatId" : 1, "message": 1, "type": 1, "time": 1, "flag": 0}
                jsonObj['chatId'] = i.chat_id
                jsonObj['message'] = i.message
                jsonObj['type'] = i.message_type
                jsonObj['time'] = i.date_modified.timestamp()
                jsonObj['flag'] = i.flag
                jsonObjRoot["messages"].append(jsonObj)
            print(jsonObjRoot)
            return JsonResponse(jsonObjRoot)
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chatlist error'})




