# from django.shortcuts import render

# Create your views here.
# import requests
# import json
import datetime, json


from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from auth.models import Users, ChatList
from .models import chat
from addFriends.models import chatMember
from Contact.models import Profile
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
            # print(token)
            user = Users.objects.get(token=token)
            # print(user.user_id)
            cl = ChatList.objects.filter(user_id=user.user_id, chat_id=chatId)
            if len(cl)==0:
                return JsonResponse({'error': 'User not in this chat'})

            for i in cl:
                i.flag = 0
                i.save()

            c = chat.objects.filter(chat_id=chatId).order_by('-date_added')
            # print(user.user_id)
            member = chatMember.objects.get(id=i.chat_id[11:]).member_id
            friend = Users.objects.get(user_id=exclude(user.user_id, member)[0])
            friendp = Profile.objects.get(email=friend.email)
            userp = Profile.objects.get(email=user.email)
            ju = {"email": 0, "name":0, "image":0, 'desc':0}
            ju['email']=friendp.email
            ju['name'] = friendp.name
            ju['image'] = friendp.profile_img_str
            ju['desc'] =friendp.profile_description
            jsonObjRoot = { "userData":ju, "messages": [], 'error':''}
            for i in c:
                juser = {"user_email" :1, "name": 1, "image":0}
                jsonObj = { "_id": 1, "user" : juser, "message": 1, "media":1,"type": 1, "latitude": 0, "longitude":0, "time": 1}
                jsonObj['_id'] = i.id
                if i.user_email==user.email:
                    juser['user_email'] = user.email
                    juser['name'] = userp.name
                else:
                    juser['user_email'] = friend.email
                    juser['name'] = friendp.name
                jsonObj['user'] = juser
                jsonObj['media'] = i.media
                jsonObj['message'] = i.message
                jsonObj['type'] = i.message_type
                jsonObj['latitude'] = i.latitude
                jsonObj['longitude'] = i.longitude
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
        # print(requests.json())
        message = requests.POST.get('message')
        token = requests.POST.get('token')
        chatId = requests.POST.get('chatId')
        mtype = requests.POST.get('type')
        email = requests.POST.get('email')
        media = requests.POST.get('media')

        # print("Here:")
        # print(token)

        if message is None:
            message = requests.GET.get('message')
        if token is None:
            token = requests.GET.get('token')
        if chatId is None:
            chatId = requests.GET.get('chatId')
        if mtype is None:
            mtype = requests.GET.get('type')
        if email is None:
            email = requests.GET.get('email')
        if media is None:
            media = requests.GET.get('media')

        if token is None:
            try:
                jsonObj = json.loads(requests.body)
                token = jsonObj['token']
                message = jsonObj['message']
                token = jsonObj['token']
                chatId = jsonObj['chatId']
                mtype = jsonObj['type']
                email = jsonObj['email']
                media = jsonObj['media']
            except Exception as e:
                print(e)
                return {"error" : "Failed to parse data"}


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

            msgn = chat(chat_id=chatId, user_name=user.user_name, user_email=email, message=message, message_type=mtype, media=media, user_id=user.user_id)
            msgn.save()
            return JsonResponse({'success' : 'send success', 'error':''})
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chat error'})


    @classmethod
    def put(self, requests):
        _id = requests.GET.get('_id')
        token = requests.GET.get('token')
        chatId = requests.GET.get('chatId')

        if _id is None:
            jsonObj = json.loads(requests.body)
            token = jsonObj['token']
            _id = jsonObj['_id']
            chatId = jsonObj['chatId']

        # print(token)
        # print(_id)

        try:
            user = Users.objects.get(token=token)
            if user.user_id in chatMember.objects.get(id=chatId[11:]).member_id:
                chat.objects.get(id=_id).delete()
                return JsonResponse({'success': 'delete success'})
            else:
                return JsonResponse({'error': 'user not in this chat'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'delete error'})



class chatlist(View):

    @classmethod
    def get(self, requests):
        token = requests.GET.get('token')
        # print(token)
        try:
            user = Users.objects.get(token=token)
            cl = ChatList.objects.filter(user_id=user.user_id).order_by('-date_modified')
            jsonObjRoot = { "chats": [],'error':''}
            for i in cl:
                jsonObj = { "chatId" : 0, "name": 0, "message": 0, "type": 1, "time": 0, "flag": 0, "image":0}
                member = chatMember.objects.get(id=i.chat_id[11:]).member_id
                friend = Users.objects.get(user_id=exclude(user.user_id, member)[0])
                friendp = Profile.objects.get(email=friend.email)
                jsonObj['chatId'] = i.chat_id
                jsonObj['message'] = i.message
                jsonObj['type'] = i.message_type
                jsonObj['time'] = i.date_modified
                jsonObj['flag'] = i.flag
                jsonObj['name'] = friendp.name
                jsonObj['image'] = friendp.profile_img_str
                jsonObjRoot["chats"].append(jsonObj)

            # print(jsonObjRoot)
            return JsonResponse(jsonObjRoot)
        except Exception as e:
            print(e)
            return JsonResponse({"error" : "chatlist error"})



def exclude(n, arr):
    for i in arr:
        if i==n:
            arr.remove(n)
            return arr
    return arr
