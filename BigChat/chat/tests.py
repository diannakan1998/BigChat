from django.test import TransactionTestCase, Client
from .models import chat
from auth.models import Users, ChatList
import datetime, json


# Using the standard RequestFactory API to create a form POST request

class chatTest(TransactionTestCase):
	def setUp(self):
		print("Chat Test: setup")
		Users.objects.create(token='Test1', email='testemail1', user_name='test1')
		user = Users.objects.get(token='Test1')
		chat.objects.create(chat_id='chat_test_1', user_id=user.user_id, user_name='test1', user_email='testemail1', message='t1', message_type=1)	
		chat.objects.create(chat_id='chat_test_1', user_id=user.user_id, user_name='test1', user_email='testemail1', message='t2', message_type=1)	
		ChatList.objects.create(chat_id='chat_test_1', user_id=user.user_id, message='t2', message_type=1,flag=1, name='test1', date_added=datetime.datetime.now(),  date_modified=datetime.datetime.now())

	def testGetMessages(self):	
		print("Chat Test:")
		c = Client()
		res = c.get('/chat/chatlist/', {'token':'Test1'})
		data = res.json()
		# print(data)
		self.assertEqual(data['chats'][0]['message'], 't2')
		print("Test 1 Status: Passed")
		self.assertEqual(data['chats'][0]['flag'], 1)
		print("Test 2 Status: Passed")

		# print("chatTest:chat history get ")
		c = Client()
		request = c.get('/chat/MessageHistory/', {'token': 'Test1', 'chatId': 'chat_test_1'})
		data = request.json()
		# print(data)
		self.assertEqual(data['messages'][0]['user']['user_email'], 'testemail1')
		print("Test 3 Status: Passed")
		self.assertEqual(data['messages'][0]['user']['name'], 'test1')
		print("Test 4 Status: Passed")
		self.assertEqual(data['messages'][0]['message'],'t2')
		print("Test 5 Status: Passed")

		# print("chatTest: chatlist2")
		c = Client()
		res = c.get('/chat/chatlist/', {'token':'Test1'})
		data = res.json()
		# print(data)
		self.assertEqual(data['chats'][0]['flag'], 0)
		print("Test 6 Status: Passed")

	# def testSendMessages(self):
		# print("chatTest: chat history send")
		js = {'token': 'Test1', 'chatId': 'chat_test_1', 'message':'send1', 'type':1, 'media':'', 'email':'testemail1'}
		c = Client()
		res = c.post('/chat/MessageHistory/',js)
		data = res.json()
		# print(data)
		self.assertEqual(data['success'], 'send success')
		print("Test 7 Status: Passed")

		# print("chatTest: chatlist3")
		c = Client()
		res = c.get('/chat/chatlist/', {'token':'Test1'})
		data = res.json()
		# print(data)
		self.assertEqual(data['chats'][0]['flag'], 1)
		print("Test 8 Status: Passed")
		self.assertEqual(data['chats'][0]['message'], 'send1')
		print("Test 9 Status: Passed")
		self.assertEqual(data['chats'][0]['type'], 1)	
		print("Test 10 Status: Passed")


	# def testGetNoUser(self):
		# print("chatTest: get history err test")
		c = Client()
		res = c.get('/chat/MessageHistory/', {'token': 'Test2', 'chatId': 'chat_test_1'})
		data = res.json()
		# print(data)
		self.assertEqual(data['error'], 'chat error')
		print("Test 11 Status: Passed")

	# def testPostError(self):
		# print("chatTest: send message err test")
		c = Client()
		res = c.post('/chat/MessageHistory/', {'token': 'Test2', 'chatId': 'chat_test_1', 'message':'send1', 'type':1, 'media':'', 'email':'testemail1'})
		data = res.json()
		# print(data)
		self.assertEqual(data['error'], 'chat error')
		print("Test 12 Status: Passed")

		print("All Chat Test Passed")


	def testSnapDel(self):
		print("Snap Delete Test:")
		c = Client()
		res = c.put('/chat/MessageHistory/', {'token': 'Test1', 'chatId': 'chat_test_1', 'type':4, 'id':1})
		data=res.json()
		print(data)
		self.assertEqual(data['success'], 'delete success')
		# print("Test 1 Status: Failed")


