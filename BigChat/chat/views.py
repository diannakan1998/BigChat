# from django.shortcuts import render

# Create your views here.
# import request
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
    # snap chat deleting 
    @classmethod
    def put(self, request):
        # prit("here")
        _id = request.GET.get('_id')
        token = request.GET.get('token')
        # chatId = request.GET.get('chatId')

        if _id is None:
            jsonObj = json.loads(request.body)
            token = jsonObj['token']
            _id = jsonObj['_id']
            # chatId = jsonObj['chatId']

        # print(token)
        # print(_id)

        try:
            user = Users.objects.get(token=token)
            msg = chat.objects.get(id=_id)
            chatId = msg.chat_id
            # checking if user is in this chat
            if user.user_id in chatMember.objects.get(id=msg.chat_id[11:]).member_id:
                msg.delete()
                cl = ChatList.objects.get(user_id=user.user_id, chat_id=chatId)
                cl.flag = 0
                cl.message = '[Snap Viewed]'
                cl.save()
                # print(i.message)

                return JsonResponse({'success': 'delete success'})
            else:
                return JsonResponse({'error': 'user not in this chat'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'delete error'})

    # example return json
    # { "userData":{"email": 0, "name":0, "image":0, 'desc':0}, "messages": [
    # { "_id": 1, "user" : {"user_email" :1, "name": 1, "image":0}, "message": 1, "media":1,"type": 1, "latitude": 0, "longitude":0, "time": 1}
    # ], 'error':''}
    
    @classmethod
    def get(self, request):
        chatId = request.GET.get('chatId')
        token = request.GET.get('token')
        try:
            # print(token)
            user = Users.objects.get(token=token)
            # print(user.user_id)
            # checking if user is in this chat
            cl = ChatList.objects.filter(user_id=user.user_id, chat_id=chatId)
            if len(cl)==0:
                return JsonResponse({'error': 'User not in this chat'})

            for i in cl:
                i.flag = 0
                i.save()

            c = chat.objects.filter(chat_id=chatId).order_by('-date_added')
            # print(user.user_id)
            # rendering user info
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
                jsonObj = { "_id": 1, "user" : juser, "token":0, "message": 1, "media":1,"type": 1, "latitude": 0, "longitude":0, "time": 1}
                jsonObj['_id'] = i.id
                if i.user_email==user.email:
                    juser['user_email'] = user.email
                    juser['name'] = userp.name
                else:
                    juser['user_email'] = friend.email
                    juser['name'] = friendp.name
                jsonObj['token'] = token
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

# send message and store in database
# example request chat/MessageHistory/?message=ss&token=token1&chatId=2&type+1&email=ddd@email&media=img&latitude=12&longitude=13
    @classmethod
    def post(self, request):
        # print(request.json())
        message = request.POST.get('message')
        token = request.POST.get('token')
        chatId = request.POST.get('chatId')
        mtype = request.POST.get('type')
        email = request.POST.get('email')
        media = request.POST.get('media')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # print("Here:")
        # print(token)

        if message is None:
            message = request.GET.get('message')
        if token is None:
            token = request.GET.get('token')
            latitude = request.GET.get('latitude')
            longitude=request.GET.get('longitude')
        if chatId is None:
            chatId = request.GET.get('chatId')
        if mtype is None:
            mtype = request.GET.get('type')
        if email is None:
            email = request.GET.get('email')
        if media is None:
            media = request.GET.get('media')

        if token is None:
            try:
                jsonObj = json.loads(request.body)
                token = jsonObj['token']
                message = jsonObj['message']
                token = jsonObj['token']
                chatId = jsonObj['chatId']
                mtype = jsonObj['type']
                email = jsonObj['email']
                media = jsonObj['media']
                latitude = jsonObj['latitude']
                longitude = jsonObj['longitude']
            except Exception as e:
                print(e)
                return {"error" : "Failed to parse data"}


        try:
            user = Users.objects.get(token=token)
            print(chatId)
            cl = ChatList.objects.filter(chat_id=chatId)

            for i in cl:

                i.message=message
                i.message_type=mtype
                i.flag=1
                i.email=email
                i.date_modified=datetime.datetime.now()
                i.save()
                print(i.message)


            msgn = chat(chat_id=chatId, user_name=user.user_name, user_email=email, message=message, message_type=mtype, media=media, user_id=user.user_id, latitude=latitude, longitude=longitude)
            msgn.save()

            return JsonResponse({'success' : 'send success', 'error':''})
        except Exception as e:
            print(e)
            return JsonResponse({'error' : 'chat error'})





# example return 
# { "chats": [{ "chatId" : 0, "name": 0, "message": 0, "type": 1, "time": 0, "flag": 0, "image":0}],'error':''}
class chatlist(View):

    @classmethod
    def get(self, request):
        token = request.GET.get('token')
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
