from django.test import TransactionTestCase
from django.test import Client

from auth.models import Users
from auth.models import ChatList
from auth.views import checkForNewUser, findUser, updateToken, addUser, processUpdateTokenRequest, processAuthRequest


class UserTestCase(TransactionTestCase):
    def setUp(self):
        Users.objects.create(email="test@email.com", token="Token1")

    def test_auth_views(self):

        # Testing Finding User
        self.assertEqual(findUser("testing@email.com", "Token5"), False)
        self.assertEqual(findUser("test@email.com", "Token1"), True)

        # Testing addUser
        self.assertEqual(addUser("testing@email.com", "Token5"), {'success': "Succesfully added new user"})
        self.assertEqual(addUser("testingemail.com", "Token5"), {'error': "Failed to add user."})

        # Testing Update Token
        self.assertEqual(updateToken("John", "test@test.com", "1", "2", "3", "google"), {'error': 'invalid_token', 'error_description': 'Invalid Value'})
        self.assertEqual(updateToken("John", "test@test.com", "1", "2", "3", "facebook"), {'error': 'Invalid OAuth access token.'})

        # Testing Check for new users
        self.assertEqual(checkForNewUser("test@email.com", "Token1"), {'success': 'user exists', 'newUser': 'false'})
        self.assertEqual(checkForNewUser("test2@email.com", "Token2"), {'success': "Succesfully added new user"})

        # Testing REST APIs (Should fail...)
        c = Client()
        response = c.get('/auth/authenticate/', {'name': 'John', 'email': 'test@email.com', 'app_id':'5', 'token':'Token1','authType':'facebook'})
        response = c.post('/auth/authenticate/', {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'token':'Token1','authType':'google'})

        response = c.put('/auth/authenticate/', {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'old_token':'Token1', 'new_token': 'Token20', 'authType':'google'})
        response = c.put('/auth/updateToken/', {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'new_token': 'Token20', 'authType':'google'})
        shouldBe = b'{"error": "Cannot process with no old token"}'
        self.assertEqual(response.content, shouldBe)

        shouldBe = b'{"error": "Cannot process with no old token"}'
        response = c.put('/auth/updateToken/', {'name': 'John', 'email': 'test@email.com', 'app_id':'10', 'old_token': 'Token1', 'authType':'google'})
        self.assertEqual(response.content, shouldBe)
