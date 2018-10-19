from django.shortcuts import render

# Create your views here.
import requests
import json


from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

# from auth.models import Users


def index(request):
    return HttpResponse("Auth POST")


class Authenticate(View):
    # model = models.Users

    def get(self, request):
        return processAuthRequest(request)

    def post(self, request):
        return processAuthRequest(request)


class updateUserToken(View):

    def get(self, request):

        status = processUpdateTokenRequest(request)
        if status is True:
            return HttpResponse("updateUserToken GET")
        else:
            return status

    def post(self, request):

        status = processUpdateTokenRequest(request)
        if status is True:
            return HttpResponse("updateUserToken GET")
        else:
            return status

    def put(self, request):

        status = processUpdateTokenRequest(request)
        if status is True:
            return HttpResponse("updateUserToken GET")
        else:
            return status


def processAuthRequest(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
    user_id = request.GET.get("user_id")
    app_id = request.GET.get("app_id")
    token = request.GET.get("token")
    authType = request.GET.get("authType")

    status = auth(name, email, user_id, app_id, token, authType)

    if "true" == status.success:
        checkForNewUser(email, user_id, token)


def processUpdateTokenRequest(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
    user_id = request.GET.get("user_id")
    app_id = request.GET.get("app_id")
    old_token = request.GET.get("old_token")
    new_token = request.GET.get("new_token")
    authType = request.GET.get("authType")

    return updateToken(name, email, user_id, app_id, old_token, new_token, authType)


def auth(name, email, user_id, app_id, token, authType):

        #  if name is None:
        #     return JsonResponse( { 'error' : 'Cannot process with no name' } )

        #  if email is None:
        #     return JsonResponse( { 'error' : 'Cannot process with no email' } )

        #  if app_id is None:
        #     return JsonResponse( { 'error' : 'Cannot process with no app_id' } )

        #  if user_id is None:
        #     return JsonResponse( { 'error' : 'Cannot process with no user_id' } )

    if token is None:
        return JsonResponse({'error': 'Cannot process with no token'})

    if authType is None:
        return JsonResponse({'error': 'Cannot process with no authType'})

        #  print (name)
        #  print (email)
        #  print (user_id)
        #  print (app_id)
        #  print (token)
        #  print (authType)
    try:

         if authType == "google":
             url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=" + token
             req = requests.post(url)
 
             jsonReq = json.loads(req.text)
 
             if jsonReq.error is Not None or jsonReq.error != "":
                 return jsonReq

             f = open('google_key.json')
             googleKey = json.load(f)

             if jsonReq.issued_to == googleKey.KEY and jsonReq.email == email and user_id == jsonReq.user_id:
                 return JsonResponse({"success": "BigChat true"})
             else:
                 return JsonResponse({"error": "BigChat false"})

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

             if jsonReq.error is Not None or jsonReq.error != "" or jsonReq_app_id.error is Not None or jsonReq_app_id.error != "":
                 return jsonReq

             f = open('facebook_key.json')
             facebookKey = json.load(f)
             jsonReq.email = jsonReq.email.replace("\u0040", "@")

             if jsonReq_app_id.id == facebookKey.KEY and jsonReq.email == email and user_id == jsonReq.id:
                 return JsonResponse({"success": "true"})
             else:
                 return JsonResponse({"error": "BigChat false"})

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
             return JsonResponse({'error': "Authenticate GET - Invalid Authentication Type."})

    except Exception:
        return JsonResponse({"error": "Caught an exception..."})


# Checks and adds new users
def checkForNewUser(email, user_id, token):

    user_exists = findUser(email)

    if user_exists == False:
        return addUser(email, user_id, token)

    else:
        return False


def findUser(email, token):
    # TODO: implement

    # # Get all Users...
    # Users.objects.all()

    # Get Users...
    try:
        #  user = Users(email=email, token=token)
        #  user = user.objects
        print("TODO")
    except Exception:
        return False

    if user is None:
        return False
    else:
        return user


def updateToken(name, email, user_id, app_id, old_token, new_token, authType):
    # TODO: implement
    # Get Users...
    try:
        auth(name, email, user_id, app_id, new_token, authType)
        #  user = Users(email=email, user_id=user_id, token=old_token)
        #  user = user.objects
        #  user.token = new_token
        #  user.save()
        return JsonResponse({'status': "Succesfully updated token"})
    except Exception:
        return JsonResponse({'error': "Failed to updated token"})


def addUser(email, user_id, token):

    # TODO: implement

    # Adds Users...
    try:

        #  user = Users(email=email, user_id=user_id, token=token)
        #  user.save()

        return JsonResponse({'status': "Succesfully added user"})

    except Exception:
        return JsonResponse({'error': "Failed to add user"})
