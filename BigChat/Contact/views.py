# from django.shortcuts import render

# Create your views here.
# import requests
from .models import Contact
from auth.models import Users
# from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
# from django.core import serializers

def index(request):
     return HttpResponse("Contact POST")

class Contacts(View):

    @classmethod
    def get(self, request):
        token = request.GET.get("token")
        # print(token)
        return JsonResponse(getContact(token))


def getContact(token):
    try:
        user =  Users.objects.get(token=token)
        # print(user.user_id)
        frd = Contact.objects.get(user_id=user.user_id)
        jsonObj = { "contact" : []}
        print(frd.friend_id)
        for i in frd.friend_id:
            jo = {"email": 1, 'name': 1, 'image':1}
            f = Users.objects.get(user_id=i)
            jo['email'] = f.email
            jo['name'] = f.user_name
            jo['image'] = f.profile_img
            jsonObj['contact'].append(jo)
        # print(jsonObj)
        return jsonObj
    except Exception as e:
        # print(e)
        return {'error': "Failed to get contact."}


class Profile(View):

    @classmethod
    def get(self, request):
        try:
            email = request.GET.get("email")
            print(email)
            user = Users.objects.get(email=email)
            json = {"email":0, "name":0, "image":0, "error":''}
            json['email'] = user.email
            json['name'] = user.user_name
            json['image'] = user.profile_img
            return JsonResponse(json)
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Failed to get profile"})

    @classmethod
    def post(self, request):
        try:
            token=request.GET.get("token")
            email = request.GET.get("email")
            image = request.GET.get("image")
            name = request.GET.get("name")
            print(token)
            user = Users.objects.get(token=token, email=email)
            user.profile_img = image
            user.user_name = name
            user.save()

            json = {"email":email, "name":name, "image":image, "error":''}
            return JsonResponse(json)
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Failed to change profile"})

#