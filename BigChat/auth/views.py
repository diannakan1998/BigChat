from django.shortcuts import render

# Create your views here.
import requests, json, uuid

from django.db import IntegrityError
from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.generic import View


# from . import models
from .models import Users
from .models import getChatListModel

def index(request):
    return HttpResponse("Auth POST")


class Authenticate(View):
    # model = models.Users

    def get(self, request):
        return JsonResponse(processAuthRequest(request))

    def post(self, request):
        return JsonResponse(processAuthRequest(request))


class updateUserToken(View):

    def get(self, request):

        status = processUpdateTokenRequest(request)
        if status is True:
            return HttpResponse("updateUserToken GET")
        else:
            return JsonResponse(status)

    def post(self, request):

        status = processUpdateTokenRequest(request)
        if status is True:
            return HttpResponse("updateUserToken GET")
        else:
            return JsonResponse(status)

    def put(self, request):

        status = processUpdateTokenRequest(request)
        if status is True:
            return HttpResponse("updateUserToken GET")
        else:
            return JsonResponse(status)


def processAuthRequest(request):
     name = request.GET.get("name")
     email = request.GET.get("email")
     app_id = request.GET.get("app_id")
     token = request.GET.get("token")
     authType = request.GET.get("authType")

     status = auth(name, email, app_id, token, authType)

     if 'success' in status:
        return checkForNewUser(email, token)
     else:
         return status
    


def processUpdateTokenRequest(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
    app_id = request.GET.get("app_id")
    old_token = request.GET.get("old_token")
    new_token = request.GET.get("new_token")
    authType = request.GET.get("authType")

    if old_token is None:
         return {'error': 'Cannot process with no old token'}
    if new_token is None:
         return {'error': 'Cannot process with no new token'}

    return updateToken(name, email, app_id, old_token, new_token, authType)


def auth(name, email, app_id, token, authType):

     # name can be null, not mandatory...
     #  if name is None:
        #  return { 'error' : 'Cannot process with no name' }

     print (name)
     print (email)
     print (app_id)
     print (token)
     print (authType)

     if email is None:
         return { 'error' : 'Cannot process with no email' }

     # Can be obtained from the access token
     #  if app_id is None:
        #  return JsonResponse( { 'error' : 'Cannot process with no app_id' } )

     if token is None:
         return {'error': 'Cannot process with no token'}

     if authType is None:
         return {'error': 'Cannot process with no authType'}


     try:

         if authType == "google":
             url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=" + token
             req = requests.post(url)
 
             jsonReq = json.loads(req.text)
 
             if 'error' in jsonReq:
                 return jsonReq

             f = open('google_key.json')
             googleKey = json.load(f)

             if 'issued_to' in jsonReq and 'email' in jsonReq:
                 if jsonReq['issued_to'] == googleKey['KEY'] and jsonReq['email'] == email:
                     return {"success": "BigChat true"}
                 else:
                     return {"error": "BigChat false"}
             else:
                 return {"error": "Missing data from Google's API..."}

             # Success Message Example
             #  {
             #     "issued_to": "KEY",
             #     "audience": "KEY",
             #     "user_id": "user.id",
             #     "scope": "https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email",
             #     "expires_in": 3389,
             #     "email": "cpen321.bigchat@gmail.com",
             #     "verified_email": true,
             #     "access_type": "online"
             # }

             # Error Message Example
             # {
             #      "error": "invalid_token",
             #      "error_description": "Invalid Value"
             # }

         elif authType == "facebook":
             url = "https://graph.facebook.com/me/?fields=name,id,email&access_token=" + token
             req = requests.get(url)

             url = "https://graph.facebook.com/app/?access_token=" + token
             req_app_id = requests.get(url)

             jsonReq = json.loads(req.text)
             jsonReq_app_id = json.loads(req_app_id.text)

             print(jsonReq)
             print(jsonReq_app_id)

             # TODO: Remove
             return {"success": "BigChat true"}


             if 'error' in jsonReq:
                 return {"error": jsonReq['error']['message'] }

             if 'error' in jsonReq_app_id:
                 return {"error": jsonReq_app_id['error']['message'] }


             f = open('facebook_key.json')
             facebookKey = json.load(f)
             jsonReq.email = jsonReq.email.replace("\u0040", "@")

             print("Facebook auth 1")
             if 'id' in jsonReq_app_id and 'KEY' in facebookKey and 'email' in jsonReq:
                 if jsonReq_app_id['id'] == facebookKey['KEY']and jsonReq['email'] == email:
                     return {"success": "BigChat true"}
                 else:
                     return {"error": "BigChat false"}
             else:
                 return {"error": "Missing data from Facebook's API..."}

            # Success Message Examples
            # {
            #    "name": "Harminder Kandola",
            #    "id": "USER_ID",
            #    "email": "harminderk\u0040hotmail.ca"
            # }

            #  {
            #    "link": "https://www.facebook.com/games/?app_id=KEY",
            #     "name": "BigChat",
            #    "id": "KEY"
            # }

            # Error Message Example
            # {"error":{"message":"Expected 1 '.' in the input between the postcard and the payload","type":"OAuthException","code":190,"fbtrace_id":"GYHrVZqj0Ne"}}

         else:
             return {'error': "Authenticate GET - Invalid Authentication Type."}

     except Exception:
         return {"error": "Caught an exception..."}


# Checks and adds new users
def checkForNewUser(email, token):

    user_exists = findUser(email, token)

    if user_exists == False:
        return addUser(email, token)
    else:
        return {"success": "user exists", "newUser": "false"}


def findUser(email, token):

    # Get Users...
     try:
         # Throws an expection if zero or more than one found
         user = Users.objects.get(email=email)
         user.token = token
         user.save()
         return True
     except Exception:
         return False




def updateToken(name, email, app_id, old_token, new_token, authType):
    # TODO: implement
    # Get Users...
     try:
         status = auth(name, email, app_id, new_token, authType)
         if 'error' in status:
             return status
         user = Users.objects.get(email=email)
         user.token = new_token
         user.save()
         return {'status': "Succesfully updated token"}
     except Exception:
        return {'error': "Failed to update token. User not found."}


def addUser(email, token):
    # Adds Users...
     try:
         # Adding the user entry
         user = Users(email=email, token=token)
         user.save()
         user_id = user.user_id
         user.chat_list_id = "chat_list_" + user_id
         user.save()

         # Creating the chat list table
         chatList = getChatListModel(user.chat_list_id)
         chatList.save()
         return {'success': "Succesfully added new user"}

     except Exception:
         return {'error': "Failed to add user."}


         
