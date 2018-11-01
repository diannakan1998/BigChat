# from django.shortcuts import render

# Create your views here.
# import requests
# import json
import datetime


from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from auth.models import Users, ChatList
from .models import chatModel
# from django.db import connection


def index(request):
    # cursor = connection.cursor()
    # cursor.execute(''' ''')
    return HttpResponse("chat POST")



class MessageHistory(View):

    @classmethod
    def get(self, requests):
        chatId = requests.GET.get('chatId')
        token = requests.GET.get('token')
        try:
            user = Users.objects.get(token=token)
            # listname = "chat_list_"+str(user.user_id)
            cl = ChatList.objects.filter(user_id=user.user_id, chat_id=chatId)
            for i in cl:
                i.flag = 0
                i.save()

            # cursor = connection.cursor()
            # cursor.execute('''UPDATE ''' + listname + ''' SET flag=0 WHERE chat_id = \''''+ chatId + '''\';''')
            # print(user.user_id)
            chats = chatModel(chatId)
            # print(chatId)
            c = chats.objects.all().order_by('-date_added')

            jsonObjRoot = { "messages": [], 'error':''}
            for i in c:
                juser = {"user_email" :1, "name": 1}
                jsonObj = { "_id": 1, "user" : juser, "message": 1, "media":1,"type": 1, "time": 1}
                jsonObj['_id'] = i.id
                juser['user_email'] = i.user_email
                juser['name'] = i.user_email
                jsonObj['user'] = juser
                jsonObj['media'] = i.media
                jsonObj['message'] = i.message
                jsonObj['type'] = i.message_type
                # print(i.date_added.date())
                # print(str(i.date_added.time())[0:8])
                # print(datetime.datetime.now().date())
                # DateTime dt = DateTime.ParseExact(dateString, "yyyy-MM-dd HH:mm::ss.ssssss", CultureInfo.InvariantCulture);
                # if datetime.datetime.now().date() == i.date_added.date():
                #     jsonObj['time'] = str(i.date_added.datetime())
                # else:
                jsonObj['time'] = i.date_added
                # jsonObj['time'] = i.date_added.
                jsonObjRoot["messages"].append(jsonObj)
            # print(jsonObjRoot)
            return JsonResponse(jsonObjRoot)
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chat error'})

    @classmethod
    def post(self, requests):
        message = requests.GET.get('message')
        token = requests.GET.get('token')
        chatId = requests.GET.get('chatId')
        mtype = requests.GET.get('type')
        email = requests.GET.get('email')
        media = requests.GET.get('media')
        print(message)
        print(token)
        print(media)
        print(mtype)
        try:
            user = Users.objects.get(token=token)
            # print(user.chat_list_id)
            cl = ChatList.objects.filter(chat_id=chatId)
            for i in cl:
                i.message=message
                i.message_type=mtype
                i.flag=1
                i.email=email
                i.date_modified=datetime.datetime.now()
                i.save()
            # listname = "chat_list_"+str(user.user_id)
            # cursor = connection.cursor()
            # cursor.execute('''UPDATE '''+listname+''' SET message=\''''+message+'''\', '''+'''message_type='''+str(mtype)+''', flag=1, date_modified=NOW() WHERE chat_id=\''''+chatId+'''\';''')
            chat = chatModel(chatId)
            msgn = chat(user_email=email, message=message, message_type=mtype, media=media, user_id=user.user_id)
            msgn.save()
            return JsonResponse({'success' : 'send success', 'error':''})
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chat error'})


class chatlist(View):

    @classmethod
    def get(self, requests):
        token = requests.GET.get('token')
        try:
            user = Users.objects.get(token=token)
            cl = ChatList.objects.filter(user_id=user.user_id).order_by('-date_modified')
            # print(cl)
            jsonObjRoot = { "chats": [],'error':''}
            for i in cl:
                jsonObj = { "chatId" : 1, "name": 1, "message": 1, "type": 1, "time": 1, "flag": 0}
                jsonObj['chatId'] = i.chat_id
                jsonObj['message'] = i.message
                jsonObj['type'] = i.message_type
                jsonObj['time'] = i.date_modified
                jsonObj['flag'] = i.flag
                jsonObj['name'] = i.name
                jsonObjRoot["chats"].append(jsonObj)
            return JsonResponse(jsonObjRoot)
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chatlist error'})
