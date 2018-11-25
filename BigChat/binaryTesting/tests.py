from django.test import TransactionTestCase
from django.test import Client

import json, os

from binaryTesting.models import media

class BinaryTesting(TransactionTestCase):
    def setUp(self):
        # Users.objects.create(email="test@email.com", token="Token1")
        print ("Hello")
    def test_binary(self):
        print ("World")
        print (os.getcwd())
        file_b = open("binaryTesting/example.png", "rb").read()
        media.objects.create(user_id="1", mediab=file_b, message_type=1)

        entry = media.objects.get(user_id="1")
        print (entry)
        print (entry.mediab)
