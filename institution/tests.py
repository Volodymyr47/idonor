from django.test import TestCase, Client


import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idonor.settings')

import django
from django.conf import settings

if not settings.configured:
    django.setup()

from donor.models import QuestionCategory, Question


class TestInstitution(TestCase):
    fixtures = ['../fixtures.json']

    def setUp(self):
        self.c = Client()

    def test_category_post(self):
        response = self.c.post('/institution/categories/', {'category_name': 'New Category'})
        self.assertEqual(response.status_code, 200)

    def test_category_edit(self):
        response = self.c.post('/institution/category/2/edit/', {'new_name': 'NewName'})
        self.assertEqual(response.status_code, 301)

    def test_category_delete(self):
        pass

