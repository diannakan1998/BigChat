# from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from auth.models import Users
from Contact.models import Contact

def index(request):
    return HttpResponse("AddFriends Index")


class addFriends(View):

    @classmethod
    def post(self, request):
        return JsonResponse(friendController(request, "add"))
    @classmethod
    def delete(self, request):
        return JsonResponse(friendController(request, "remove"))


def friendController(request, requestType):
     token = request.GET.get("token")
     email = request.GET.get("email")
     friendEmail = request.GET.get("friendEmail")

     try:
         user = Users.objects.get(email=email, token=token)
         friend = Users.object.get(email=friendEmail)

         user_id = user.user_id
         friend_id = friend.user_id

         contacts = Contact(user_id=user_id)
         contactsFriend = Contact(user_id=friend_id)

         if requestType == "add":
             addFriend(contacts, friend_id)
             addFriend(contactsFriend, user_id)
         elif requestType == "remove":
             removeFriend(contacts, friend_id)
             removeFriend(contactsFriend, user_id)
         else:
             raise Exception()

         contacts.save()
         contactsFriend.save()

         return {"success" : 200}
     except Exception:
         return {"error" : "Failed to modify contacts"}


def addFriend(contacts, friend_id):
     # NULL check
     if contacts.friend_id:
         if friend_id not in contacts.friend_id:
             contacts.friend_id.append(friend_id)
     else:
         contacts.friend_id = [friend_id]


def removeFriend(contacts, friend_id):
     # NULL check
     if contacts.friend_id and friend_id in contacts.friend_id:
         contacts.friend_id.remove(friend_id)

