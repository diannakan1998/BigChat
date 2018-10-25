from django.shortcuts import render

# Create your views here.
import requests
from .models import Contact
from auth.models import Users
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core import serializers

def index(request):
     return HttpResponse("Contact POST")

class Contacts(View):
    
    @classmethod
    def get(self, request):
        token = request.GET.get("token")
        print(token)
        return JsonResponse(getContact(token))
    
    # def addNew(self, request):
    #     token = request.GET.get("token")
    #     return JsonResponse(addNewUser(token))






def getUserId(token):
    try:
        user = Users.objects.get(token=token)
        if 'error' in user:
            return {'error': "Failed to achieve user. User not found."}
    except Exception:
        return {'error': "Failed to update token. User not found."}
    return user


def addNewUser(token):
    try:
        Contact.objects.raw('INSERT INTO contact_list (user_id, friend_id, date_added, date_modified) VALUES ((SELECT user_id FROM user_profile WHERE token = %s), NULL, NOW(), NOW())', [token])
        return {'success': 200}
    except Exception:
        return {'error': "Failed to add new user."}

def getContact(token):
    try:
        user =  Users.objects.get(token=token)
        print(user.user_id)
        frd = Contact.objects.get(user_id=user.user_id)
        print(frd.friend_id)
        jsonObj = { "friend_id" : []}
        for i in frd.friend_id:
            jo = {"email": 1}
            f = Users.objects.get(token=i)
            jo['email'] = f.email
            jsonObj['friend_id'].append(jo)
        print(jsonObj)
        return jsonObj
    except Exception as e:
        print(e)
        return {'error': "Failed to get contact."}

def addFriend(userId, friendId):
    try:
        Contact.object.raw('UPDATE contact_list SET friend_id = array_append(friend_id, %d), date_modified = NOW() WHERE user_id = %d', [friendId], [userId])
        return {'success': "Succesfully added contacts"}
    except Exception:
        return {'error': "Failed to add contact."}

