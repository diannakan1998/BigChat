from django.shortcuts import render

# Create your views here.
import requests,json


from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from . import models
from models import Users

def index( request ):
    return HttpResponse( "POST" )

class Authenticate( View ):


    name = request.GET.get("name")
    email = request.GET.get("email")
    user_id = request.GET.get("user_id")
    app_id = request.GET.get("app_id")
    token = request.GET.get("token")
    authType = request.GET.get("authType")


    # Adds Users...
    user = Users(email=email)
    user.save()

    # Get Users...
    user = Users(email=email)
    user.objects

    # Get all Users...
    Users.objects.all

    def get( self, request ):
         return auth(name, email, user_id, app_id, token, authType)

    def post( self, request):
         return auth(name, email, user_id, app_id, token, authType)


def auth(name, email, user_id, app_id, token, authType):

         if name is None:
            return JsonResponse( { 'error' : 'Cannot process with no name' } )

         if email is None:
            return JsonResponse( { 'error' : 'Cannot process with no email' } )

         if app_id is None:
            return JsonResponse( { 'error' : 'Cannot process with no app_id' } )

         if user_id is None:
            return JsonResponse( { 'error' : 'Cannot process with no user_id' } )

         if token is None:
            return JsonResponse( { 'error' : 'Cannot process with no token' } )

         if authType is None:
            return JsonResponse( { 'error' : 'Cannot process with no authType' } )

         print (name)
         print (email)
         print (user_id)
         print (app_id)
         print (token)
         print (authType)

         if authType == "google":
             url= "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="
         elif authType == "facebook":
             url = "https://graph.facebook.com/me?access_token="
         else:
              return JsonResponse( { 'error' : "Authenticate GET - Invalid Authentication Type." } )

         url = url + token
         req = requests.post(url)

         print (req)

         return HttpResponse(req, "application/json")
         

def checkForNewUser(email, user_id, token):

    user_exists = findUser(email)

    if user_exists:
        updateToken(email, user_id, token)
    else:
        addUser(email, user_id, token)



def findUser(email):
    # TODO: implement

    return False


def updateToken(email, user_id, token):
    # TODO: implement


def addUser(email, user_id, token):
    # TODO: implement


