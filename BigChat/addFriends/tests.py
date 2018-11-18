from django.test import TransactionTestCase
from django.test import Client

import json, datetime

from addFriends.models import FriendRequest
from addFriends.models import chatMember
from auth.models import Users

from addFriends.views import friendController, addFriend, removeFriend

class FriendRequestTestCase(TransactionTestCase):
    def setUp(self):
        Users.objects.create(email="test1@email.com", token="Token1")
        Users.objects.create(email="test2@email.com", token="Token2")
        Users.objects.create(email="test3@email.com", token="Token3")
        
        chatMember.objects.create(member_id=["1", "2"], date_added= datetime.datetime.now())

    def test_addFriends_views(self):
        c = Client()

        # Testing the GET friend requests
        print("AddFriends Tests: ")

        response = c.get('/addFriends/FriendRequests/', {'token': 'Token1'})
        shouldBe = b'{"success": 200, "sent": [], "recieved": []}'
        self.assertEqual(response.content, shouldBe)
        print("Test 1 Status: Passed")

        response = c.get('/addFriends/FriendRequests/', {'token': 'Token0'})
        shouldBe = b'{"error": "User or FriendRequests not found"}'
        self.assertEqual(response.content, shouldBe)
        print("Test 2 Status: Passed")

        # Testing sending Request
        data = {'token': 'Token1', 'email': 'test1@email.com', 'friendEmail':'test2@email.com'}
        response = c.post('/addFriends/FriendRequests/', data )
        shouldBe = b'{"success": 200}'
        self.assertEqual(response.content, shouldBe)
        print("Test 3 Status: Passed")

        data = {'token': 'Token1', 'email': 'test1@email.com', 'friendEmail':'test3@email.com'}
        response = c.post('/addFriends/FriendRequests/', data )
        shouldBe = b'{"success": 200}'
        self.assertEqual(response.content, shouldBe)
        print("Test 4 Status: Passed")

        # Testing deleting/decling friend reuquest
        data = {'token': 'Token3', 'email': 'test3@email.com', 'friendEmail':'test1@email.com'}
        response = c.delete('/addFriends/FriendRequests/', json.dumps(data), "application/json" )
        shouldBe = b'{"success": 200}'
        self.assertEqual(response.content, shouldBe)
        print("Test 5 Status: Passed")

        # Testing accepting friend request
        data = {'token': 'Token2', 'email': 'test2@email.com', 'friendEmail':'test1@email.com'}
        response = c.put('/addFriends/FriendRequests/', json.dumps(data), "application/json" )
        shouldBe = b'{"success": 200}'
        self.assertEqual(response.content, shouldBe)
        print("Test 6 Status: Passed")

        data = {'token': 'Token3', 'email': 'test3@email.com', 'friendEmail':'test1@email.com'}
        response = c.put('/addFriends/FriendRequests/', json.dumps(data), "application/json" )
        shouldBe = b'{"error": "Trying to add user who doesn\'t want to add you..."}'
        self.assertEqual(response.content, shouldBe)
        print("Test 7 Status: Passed")

        data = {'token': 'Token1', 'email': 'test1@email.com', 'friendEmail':'test3@email.com'}
        response = c.post('/addFriends/FriendRequests/', data)
        shouldBe = b'{"success": 200}'
        self.assertEqual(response.content, shouldBe)
        print("Test 8 Status: Passed")

        data = {'token': 'Token3', 'email': 'test3@email.com', 'friendEmail':'test1@email.com'}
        response = c.put('/addFriends/FriendRequests/', json.dumps(data), "application/json" )
        shouldBe = b'{"success": 200}'
        self.assertEqual(response.content, shouldBe)
        print("Test 9 Status: Passed")

        print("All AddFriends tests passed")
