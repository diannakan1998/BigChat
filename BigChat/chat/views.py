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

from auth.models import Users, getChatListModel
from .models import chatModel
from django.db import connection


def index(request):
    # cursor = connection.cursor()
    # cursor.execute(''' ''')
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
            listname = "chat_list_"+str(user.user_id)
            listm = getChatListModel(listname)
            cursor = connection.cursor()   
            cursor.execute('''UPDATE ''' + listname + ''' SET flag=0 WHERE chat_id = \''''+ chatId + '''\';''')
            print(user.user_id)
            chats = chatModel(chatId)
            print(chatId)
            c = chats.objects.all().order_by('date_added')

            jsonObjRoot = { "messages": [], 'error':''}
            for i in c:
                jsonObj = { "user_email" : 1, "message": 1, "type": 1, "time": 1}
                jsonObj['user_email'] = i.user_email
                jsonObj['message'] = i.message
                jsonObj['type'] = i.message_type
                jsonObj['time'] = i.date_added.timestamp()
                jsonObjRoot["messages"].append(jsonObj)
            print(jsonObjRoot)
            return JsonResponse(jsonObjRoot)
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
        print(token)
        print(chatId)
        print(mtype)
        try:
            user = Users.objects.get(token=token)
            print(user.chat_list_id)
            listname = "chat_list_"+str(user.user_id)
            cursor = connection.cursor()  
            cursor.execute('''UPDATE '''+listname+''' SET message=\''''+message+'''\', '''+'''message_type='''+str(mtype)+''', flag=1, date_modified=NOW() WHERE chat_id=\''''+chatId+'''\';''')

            chat = chatModel(chatId)
            msgn = chat(user_email=email, message=message, message_type=mtype, user_id=user.user_id)
            msgn.save()
            return JsonResponse({'success' : 'send success', 'error':''})
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chat error'})


class chatlist(View):

    def get(self, requests):
        token = requests.GET.get('token')
        try:
            user = Users.objects.get(token=token)
            cln = "chat_list_"+str(user.user_id)
            listm = getChatListModel("chat_list_"+str(user.user_id))
            print(user.user_id)
            cursor = connection.cursor()
            cursor.execute('''SELECT * FROM ''' + cln + ''' ORDER BY date_modified DESC;''')
            cl = cursor.fetchall()
            # cl = listm.objects.all().order_by('-date_modified')
            jsonObjRoot = { "chats": [],'error':''}
            for i in cl:
                # id
                # table name
                # message
                # message mtyp
                # date date_added
                # date_modified
                # flag
                jsonObj = { "chatId" : 1, "message": 1, "type": 1, "time": 1, "flag": 0}
                jsonObj['chatId'] = i[1]
                jsonObj['message'] = i[2]
                jsonObj['type'] = i[3]
                jsonObj['time'] = i[5]
                jsonObj['flag'] = i[6]
                jsonObjRoot["chats"].append(jsonObj)
            return JsonResponse(jsonObjRoot)
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chatlist error'})
