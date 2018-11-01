# from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from auth.models import Users
from Contact.models import Contact
from addFriends.models import FriendRequests
def index(request):
    return HttpResponse("AddFriends Index")


class addFriends(View):

    @classmethod
    def get(self, request):
        return JsonResponse(getFriendRequests(request))
    @classmethod
    def post(self, request):
        return JsonResponse(friendController(request, "sendAdd"))
    @classmethod
    def delete(self, request):
        return JsonResponse(friendController(request, "remove"))
    @classmethod
    def put(self, request):
        return JsonResponse(friendController(request, "add"))

def getFriendRequests(request):
    token = request.GET.get("token")
    try:
        user = Users.objects.get(token=token)
        friendRequests = FriendRequests.objects.get(user_id=user.user_id)

        friendRequests_status = {"success": 200, "Sent": [], "Recieved": []}

        for i in friendRequests.friend_requests_emails_sent:
            friendRequests_status.Sent.append(i)
        for i in friendRequests.friend_requests_emails_recieved:
            friendRequests_status.Recieved.append(i)

        return friendRequests_status
    except Exception as e:
        return {"error": "User or FriendRequests not found"}



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
             try:
                 friendRequests = FriendRequests.objects.get(user_id=user_id)
                 friend_friendRequests = FriendRequests.objects.get(user_id=friend_id)
                 if friendEmail in friendRequests.friend_requests_emails_recieved and email in friend_friendRequests.friend_requests_emails_sent:
                     addFriend(contacts, friend_id)
                     addFriend(contactsFriend, user_id)

                     friendRequests.friend_requests_emails_recieved.remove(friendEmail)
                     friend_friendRequests.friend_requests_emails_sent.remove(email)

                     friendRequests.save()
                     friend_friendRequests.save()
                 else:
                     return {"error": "Trying to add user who doesn't want to add you..."}
             except Exception:
                 return {"error": "FriendRequests entry does not exist for one or both of the users in question."}
         elif requestType == "remove":
             # TODO: remove chat history or keep it?
             removeFriend(contacts, friend_id)
             removeFriend(contactsFriend, user_id)
         elif requestType == "sendAdd":
             print ("TODO")
             friendRequests = None
             friend_friendRequests = None

             if FriendRequests.objects.filter(user_id=user_id).exists() not True:
                 friendRequests = FriendRequests(user_id=user_id)
                 friendRequests.save()

             if friend_friendRequests.objects.filter(user_id=friend_id).exists() not True:
                 friend_friendRequests = FriendRequests(user_id=friend_id)
                 friend_friendRequests.save()

             if FriendRequests.friend_requests_emails_sent:
                 if friendEmail not in FriendRequests.friend_requests_emails_sent:
                     FriendRequests.friend_requests_emails_sent.append(friendEmail)
             else:
                 FriendRequests.friend_requests_emails_sent = [friendEmail]

             if friend_friendRequests.friend_requests_emails_recieved:
                 if email not in friend_friendRequests.friend_requests_emails_recieved:
                     friend_friendRequests.friend_requests_emails_recieved.append(email)
             else:
                 friend_friendRequests.friend_requests_emails_recieved = [email]

             friendRequests.save()
             friend_friendRequests.save()

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
