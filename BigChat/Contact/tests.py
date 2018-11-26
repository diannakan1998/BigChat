from django.test import TransactionTestCase, Client
from Contact.models import Contact, Profile
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

		Profile.objects.create(email='testemail1', name='test1', profile_img_str='img1')
		Profile.objects.create(email='testemail2', name='test2', profile_img_str='img2')
		Profile.objects.create(email='testemail3', name='test3', profile_img_str='img3')
		

	def testGet(self):	
		print("Contact Test")
		c = Client()
		request = c.get('/Contact/Contacts/', {'token': 'Test1'})
		data = request.json()
		# print(data)
		self.assertEqual(data['contact'][0]['name'], 'test2')
		self.assertEqual(data['contact'][0]['image'], 'img2')
		print("Test 1 Status: Passed")
		self.assertEqual(data['contact'][1]['name'], 'test3')
		self.assertEqual(data['contact'][1]['image'], 'img3')
		print("Test 2 Status: Passed")

		# print("Contact Test: err test")
		c = Client()
		request = c.get('/Contact/Contacts/', {'token': 'Test4'})
		data = request.json()
		# print(data)
		self.assertEqual(data['error'], 'Failed to get contact.')
		print("Test 3 Status: Passed")

		print("All Contact Tests Passed")


	def testProfile(self):
		print("Profile Test")
		c=Client()
		request = c.get('/Contact/Profile/', {'email':'testemail1'})
		data = request.json()
		# print(data)
		self.assertEqual(data['name'], 'test1')
		self.assertEqual(data['image'], 'img1')
		print("Test 1 Status: Passed")

		c=Client()
		request = c.post('/Contact/Profile/', {'email': 'testemail1', 'token': 'Test1', 'image': 'imgchange', 'name': 'test1name'})
		data = request.json()
		self.assertEqual(data['name'], 'test1name')
		self.assertEqual(data['image'], 'imgchange')
		print("Test 2 Status: Passed")

		c=Client()
		request = c.post('/Contact/Profile/', {'email': 'testemail1', 'token': 'Test1', 'image': '', 'name': 'test1name'})
		data = request.json()
		p = Profile.objects.get(email='testemail1')
		self.assertEqual(p.name, 'test1name')
		self.assertEqual(p.profile_img_str, 'imgchange')
		print("Test 3 Status: Passed")

		# c=Client()
		# request = c.post('/Contact/Contacts/', {'email': 'testemail2', 'token': 'Test1', 'image': '', 'name': 'test1name'})
		# data = request.json()
		# self.assertEqual(data['error'], 'Cannot change other peoples profile')
		# print("Test 4 Status: Passed")

		print('All Profile Tests Passed')


