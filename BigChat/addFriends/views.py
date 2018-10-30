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
        return JsonResponse(addFriend(request))
    @classmethod
    def delete(self, request):
        return JsonResponse(removeFriend(request))



def addFriend(request):
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

         # NULL check
         if contacts.friend_id:
             if friend_id not in contacts.friend_id:
                contacts.friend_id.append(friend_id)
         else:
             contacts.friend_id = [friend_id]

         # NULL check
         if contactsFriend.friend_id:
             if user_id not in contactsFriend.friend_id:
                contactsFriend.friend_id.append(user_id)
         else:
             contactsFriend.friend_id = [user_id]

         return {"success" : "Added Friend"}
     except Exception:
         return {"error" : "Failed to add Friend"}



def removeFriend(request):
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

         # NULL check
         if contacts.friend_id and friend_id in contacts.friend_id:
                contacts.friend_id.remove(friend_id)

         # NULL check
         if contactsFriend.friend_id and user_id in contactsFriend.friend_id:
                contactsFriend.friend_id.remove(user_id)

         return {"success" : "Removed friend"}
     except Exception:
         return {"error" : "Failed to remove friend"}

