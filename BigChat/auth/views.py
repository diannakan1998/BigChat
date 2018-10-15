from django.shortcuts import render

# Create your views here.
import requests,json


from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from . import models

def index( request ):
    return HttpResponse( "POST" )

class Authenticate( View ):

    def get( self, request, user_id=None, token=None, authType=None ):
         app_id = request.GET.get("app_id")
         user_id = request.GET.get("user_id")
         token = request.GET.get("token")
         authType = request.GET.get("authType")
         return auth(app_id, user_id, token, authType)

    def post( self, request, user_id=None, token=None, authType=None ):
         app_id = request.GET.get("app_id")
         user_id = request.GET.get("user_id")
         token = request.GET.get("token")
         authType = request.GET.get("authType")
         return auth(app_id, user_id, token, authType)


def auth(app_id, user_id, token, authType):

         print (user_id)
         print (token)
         print (authType)

         if token is None:
            return JsonResponse( { 'errors' : { 'token' : 'cannot GET with no token' } } )

         if authType is None:
            return JsonResponse( { 'errors' : { 'authType' : 'cannot POST with no authType' } } )
            
         if app_id is None:
            return JsonResponse( { 'errors' : { 'app_id' : 'cannot POST with no app_id' } } )

         if user_id is None:
            return JsonResponse( { 'errors' : { 'user_id' : 'cannot POST with no user_id' } } )

         if authType == "google":
             url= "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="
         elif authType == "facebook":
             url = "https://graph.facebook.com/me?access_token="
         else:
              return HttpResponse( "Authenticate GET - Invalid Authentication Type." )

         url = url + token
         req = requests.post(url)

         return HttpResponse(req, "application/json")
