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
        # print(frd.friend_id)
        for i in frd.friend_id:
            jo = {"email": 1, 'name': 1}
            f = Users.objects.get(user_id=i)
            jo['email'] = f.email
            jo['name'] = f.user_name
            jsonObj['contact'].append(jo)
        # print(jsonObj)
        return jsonObj
    except Exception as e:
        # print(e)
        return {'error': "Failed to get contact."}

#