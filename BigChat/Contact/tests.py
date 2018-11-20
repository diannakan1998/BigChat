from django.test import TransactionTestCase, Client
from Contact.models import Contact
from auth.models import Users
import datetime, json


class contactTest(TransactionTestCase):
	def setUp(self):
		# if len(Users.objects.all())==0:
		print("Contact Test: setup")
		Users.objects.create(token='Test1', email='testemail1', user_name='test1')
		Users.objects.create(token='Test2', email='testemail2', user_name='test2')
		Users.objects.create(token='Test3', email='testemail3', user_name='test3')
		user1 = Users.objects.get(token='Test1')
		user2 = Users.objects.get(token='Test2')
		user3 = Users.objects.get(token='Test3')
		Contact.objects.create(user_id=user1.user_id, friend_id=[user2.user_id,user3.user_id], date_added= datetime.datetime.now())

	def testGet(self):	
		print("Contact Test")
		c = Client()
		request = c.get('/Contact/Contacts/', {'token': 'Test1'})
		data = request.json()
		# print(data)
		self.assertEqual(data['contact'][0]['name'], 'test2')
		print("Test 1 Status: Passed")
		self.assertEqual(data['contact'][1]['name'], 'test3')
		print("Test 2 Status: Passed")

		# print("Contact Test: err test")
		c = Client()
		request = c.get('/Contact/Contacts/', {'token': 'Test4'})
		data = request.json()
		# print(data)
		self.assertEqual(data['error'], 'Failed to get contact.')
		print("Test 3 Status: Passed")

		print("All Contact Tests Passed")