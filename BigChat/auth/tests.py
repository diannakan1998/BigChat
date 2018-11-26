from django.test import TransactionTestCase
from django.test import Client

import json

from auth.models import Users
from auth.models import ChatList
from auth.views import checkForNewUser, findUser, updateToken, addUser, processUpdateTokenRequest, processAuthRequest
from Contact.models import Profile


class UserTestCase(TransactionTestCase):
    def setUp(self):
        Users.objects.create(email="test@email.com", token="Token1")

    # def test(self):
        # addUser("testing2@email.com", "Token5")
        # user = Profile.objects.get(email="testing2@email.com")
        # print(user.profile_img_str)
        # print("done")

    def test_auth_views(self):

        print("Auth Tests:")
        # Testing Finding User
        self.assertEqual(findUser("testing@email.com", "Token5"), False)
        print("Test 1 Status: Passed")
        self.assertEqual(findUser("test@email.com", "Token1"), True)
        print("Test 2 Status: Passed")

        # Testing addUser
        self.assertEqual(addUser("testing@email.com", "Token5"), {'success': "Succesfully added new user","newUser": 1})
        print("Test 3 Status: Passed")
        self.assertEqual(addUser("testingemail.com", "Token5"), {'error': "Failed to add user."})
        print("Test 4 Status: Passed")

        # Testing Update Token
        self.assertEqual(updateToken("John", "test@test.com", "1", "2", "3", "google"), {'error': 'invalid_token', 'error_description': 'Invalid Value'})
        print("Test 5 Status: Passed")
        self.assertEqual(updateToken("John", "test@test.com", "1", "2", "3", "facebook"), {'error': 'Invalid OAuth access token.'})
        print("Test 6 Status: Passed")

        # Testing Check for new users
        self.assertEqual(checkForNewUser("test@email.com", "Token1"), {'success': 'user exists', 'newUser': 0})
        print("Test 7 Status: Passed")
        self.assertEqual(checkForNewUser("test2@email.com", "Token2"), {'success': "Succesfully added new user","newUser": 1})
        print("Test 8 Status: Passed")

        # Testing REST APIs (Should fail...)
        c = Client()

        response = c.get('/auth/authenticate/', {'name': 'John', 'email': 'test@email.com', 'app_id':'5', 'token':'Token1','authType':'facebook'}, "application/json")
        shouldBe = b'{"error": "Invalid OAuth access token."}'
        self.assertEqual(response.content, shouldBe)
        print("Test 9 Status: Passed")

        response = c.get('/auth/authenticate/', {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'token':'Token1','authType':'google'}, "application/json")
        shouldBe = b'{"error": "invalid_token", "error_description": "Invalid Value"}'
        self.assertEqual(response.content, shouldBe)
        print("Test 10 Status: Passed")

        response = c.post('/auth/updateToken/', {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'old_token':'Token1', 'new_token': 'Token20', 'authType':'google'})
        shouldBe = b'{"error": "invalid_token", "error_description": "Invalid Value"}'
        self.assertEqual(response.content, shouldBe)
        print("Test 11 Status: Passed")

        response = c.post('/auth/updateToken/', {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'new_token': 'Token20', 'authType':'google'})
        shouldBe = b'{"error": "Cannot process with no old token"}'
        self.assertEqual(response.content, shouldBe)
        print("Test 12 Status: Passed")

        data = {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'old_token': 'Token1', 'authType':'google'}
        shouldBe = b'{"error": "Cannot process with no new token"}'

        response = c.post('/auth/updateToken/', data)
        self.assertEqual(response.content, shouldBe)
        print("Test 13 Status: Passed")

        print("All Auth tests Passed")
