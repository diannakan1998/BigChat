# from django.shortcuts import render

# Create your views here.
import requests, json
# , uuid

# from django.db import IntegrityError
# from django.core import serializers
# from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
# from django.db import connection

# from . import models
from .models import Users

def index(request):
    return HttpResponse("Auth POST")


class Authenticate(View):
    # model = models.Users
    @classmethod
    def get(self, request):
        return JsonResponse(processAuthRequest(request))
    # @classmethod
    # def post(self, request):
    #     return JsonResponse(processAuthRequest(request))

class updateUserToken(View):

    @classmethod
    def post(self, request):

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
         # print ("auth success")
         return checkForNewUser(email, token)
     else:
         # print ("auth fail")
         return status



def processUpdateTokenRequest(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    app_id = request.POST.get("app_id")
    old_token = request.POST.get("old_token")
    new_token = request.POST.get("new_token")
    authType = request.POST.get("authType")

    if old_token is None:
         return {'error': 'Cannot process with no old token'}
    if new_token is None:
         return {'error': 'Cannot process with no new token'}

    return updateToken(name, email, app_id, old_token, new_token, authType)


def auth(name, email, app_id, token, authType):

     # name can be null, not mandatory...
     #  if name is None:
        #  return { 'error' : 'Cannot process with no name' }

     # print (name)
     # print (email)
     # print (app_id)
     # print (token)
     # print (authType)

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

             f = open('auth/google_key.json')
             googleKey = json.load(f)

             f = open('auth/google_key.json.old')
             googleKeyOld = json.load(f)

             if 'issued_to' in jsonReq and 'email' in jsonReq and 'KEY' in googleKey and 'KEY' in googleKeyOld:
                 if (jsonReq['issued_to'] == googleKeyOld['KEY'] or jsonReq['issued_to'] == googleKey['KEY']) and jsonReq['email'] == email:
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

             # print(jsonReq)
             # print(jsonReq_app_id)

             # TODO: Remove
             #  return {"success": "BigChat true"}


             if 'error' in jsonReq:
                 return {"error": jsonReq['error']['message'] }

             if 'error' in jsonReq_app_id:
                 return {"error": jsonReq_app_id['error']['message'] }

             # print ("Test0")
             f = open('auth/facebook_key.json')
             facebookKey = json.load(f)

             f = open('auth/facebook_key.json.old')
             facebookKeyOld = json.load(f)
             # print ("Test1")
             jsonReq['email'] = jsonReq['email'].replace("\u0040", "@")

             # print("Facebook auth 1")
             if 'id' in jsonReq_app_id and 'KEY' in facebookKey and 'email' in jsonReq and 'KEY' in facebookKeyOld:
                 if (jsonReq_app_id['id'] == facebookKey['KEY'] or jsonReq_app_id['id'] == facebookKeyOld['KEY']) and jsonReq['email'] == email:
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

     except Exception as e:
         # print (e)
         return {"error": "Caught an exception..."}


# Checks and adds new users
def checkForNewUser(email, token):

    user_exists = findUser(email, token)

    if user_exists == False:
        # print ("adding new user...")
        return addUser(email, token)
    else:
        return {"success": "user exists", "newUser": 0}


def findUser(email, token):

    # Get Users...
     try:
         # Throws an expection if zero or more than one found
         # print ("finding user...")
         user = Users.objects.get(email=email)
         user.token = token
         user.save()
         # print ("updated token...")
         return True
     except Exception as e:
         # print("Caught an exp in findUser")
         # print (e)
         return False




def updateToken(name, email, app_id, old_token, new_token, authType):
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
         # print ( "user: ")
         user = Users(email=email, token=token)
         user.save()
         # print ( "user: ")

         user_id = user.user_id
         # user.chat_list_id = "chat_list_" + str(user_id)
         user.save()
         # print (user.chat_list_id)
         # Creating the chat list table
         # cursor = connection.cursor()
         # cursor.execute("CREATE TABLE "+ user.chat_list_id +" ( id SERIAL, chat_id text NOT NULL, message text DEFAULT NULL, message_type integer DEFAULT NULL, date_added TIMESTAMP DEFAULT NULL, date_modified TIMESTAMP DEFAULT NULL, flag integer DEFAULT 0, name text DEFAULT NULL, PRIMARY KEY(id))", [user.chat_list_id])

         return {'success': "Succesfully added new user","newUser": 1}

     except Exception as exp:
         # print (exp)
         return {'error': "Failed to add user."}
