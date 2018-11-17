from django.test import TransactionTestCase
from django.test import Client

from addFriends.models import FriendRequest
from addFriends.models import chatMember
from auth.models import Users

from addFriends.views import getFriendRequests, friendController, addFriend, removeFriend

class FriendRequestTestCase(TransactionTestCase):
    def setUp(self):
        Users.objects.create(email="test1@email.com", token="Token1")
        Users.objects.create(email="test2@email.com", token="Token2")

        FriendRequest.objects.create(user_id="1", friend_requests_emails_recieved= ["test2@email.com"] ,friend_requests_emails_sent= ["test1@email.com"])
        FriendRequest.objects.create(user_id="2", friend_requests_emails_recieved= ["test1@email.com"] ,friend_requests_emails_sent= ["test2@email.com"])

        chatMember.objects.create(member_id=["1", "2"])

    def test_auth_views(self):
        print("TODO")
