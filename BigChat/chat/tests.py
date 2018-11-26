from django.test import TransactionTestCase, Client
from .models import chat
from auth.models import Users, ChatList
import datetime, json
from addFriends.models import chatMember
from Contact.models import Profile


# Using the standard RequestFactory API to create a form POST request

class chatTest(TransactionTestCase):
	def setUp(self):
		print("Chat Test: setup")
		Users.objects.create(token='Test1', email='testemail1')
		Users.objects.create(token='Test2', email='testemail2')

		user = Users.objects.get(token='Test1')
		user2 = Users.objects.get(token='Test2')

		chatMember.objects.create(member_id=[user.user_id,user2.user_id], date_added=datetime.datetime.now(), date_modified=datetime.datetime.now())
		cm = chatMember.objects.all()[0]
		# print(cm.member_id)
		chat.objects.create(chat_id='chat_table_'+str(cm.id), user_id=user.user_id,  user_email='testemail1', message='t1', message_type=1)	
		chat.objects.create(chat_id='chat_table_'+str(cm.id), user_id=user2.user_id, user_email='testemail1', message='t2', message_type=1)	
		chat.objects.create(chat_id='chat_table_'+str(cm.id), user_id=user.user_id, user_email='testemail1', message='img', message_type=6)	

		Profile.objects.create(email='testemail1', name='test1', profile_img_str='img1')
		Profile.objects.create(email='testemail2', name='test2', profile_img_str='img2')
		Profile.objects.create(email='testemail3', name='test3', profile_img_str='img3')
		ChatList.objects.create(chat_id='chat_table_'+str(cm.id), user_id=user.user_id, message='t2', message_type=1,flag=1, name='test1', date_added=datetime.datetime.now(),  date_modified=datetime.datetime.now())
		ChatList.objects.create(chat_id='chat_table_'+str(cm.id), user_id=user2.user_id, message='t2', message_type=1,flag=1, name='test1', date_added=datetime.datetime.now(),  date_modified=datetime.datetime.now())

		

	def testGetMessages(self):	
		print("Chat Test:")
		cm = chatMember.objects.all()[0]
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
		request = c.get('/chat/MessageHistory/', {'token': 'Test1', 'chatId': 'chat_table_'+str(cm.id)})
		data = request.json()
		# print(data)
		self.assertEqual(data['messages'][0]['user']['user_email'], 'testemail1')
		print("Test 3 Status: Passed")
		self.assertEqual(data['messages'][0]['user']['name'], 'test1')
		print("Test 4 Status: Passed")
		self.assertEqual(data['messages'][0]['message'],'img')
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
		js = {'token': 'Test1', 'chatId': 'chat_table_'+str(cm.id), 'message':'send1', 'type':1, 'media':'', 'email':'testemail1'}
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
		res = c.get('/chat/MessageHistory/', {'token': 'Test3', 'chatId': 'chat_table_'+str(cm.id)})
		data = res.json()
		# print(data)
		self.assertEqual(data['error'], 'chat error')
		print("Test 11 Status: Passed")

	# def testPostError(self):
		# print("chatTest: send message err test")
		c = Client()
		res = c.post('/chat/MessageHistory/', {'token': 'Test3', 'chatId': 'chat_table_'+str(cm.id), 'message':'send1', 'type':1, 'media':'', 'email':'testemail1'})
		data = res.json()
		# print(data)
		self.assertEqual(data['error'], 'chat error')
		print("Test 12 Status: Passed")

		print("All Chat Test Passed")


	def testSnapDel(self):
		print("Snap Delete Test:")
		cm = chatMember.objects.all()[0]
		# print(cm.id)
		msg = chat.objects.get(chat_id='chat_table_'+str(cm.id), user_email='testemail1', message='img', message_type=6)
		c = Client()
		data= {'token': 'Test1', 'chatId': 'chat_table_'+str(cm.id),'_id':msg.id}
		res = c.put('/chat/MessageHistory/', json.dumps(data), "application/json")
		data=res.json()
		# print(data)
		msga = chat.objects.filter(message_type=6)
		# print(len(msga))
		self.assertEqual(len(msga),0)
		self.assertEqual(data['success'], 'delete success')
		print("Test 1 Status: Passed")
		print("All Snap Test Passed")


