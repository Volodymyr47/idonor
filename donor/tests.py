from django.test import TestCase, Client

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idonor.settings')

import django
from django.conf import settings

if not settings.configured:
    django.setup()

from institution.models import QuestionCategory
from institution import models


class TestInstitution(TestCase):
    fixtures = ['../fixtures.json']

    def setUp(self):
        self.c = Client()

    def test_category_1_post(self):
        self.c.login(email='spec@gmail.com', password='1')
        response = self.c.post('/institution/categories/', {'category_name': 'New Category'})
        self.assertEqual(response.status_code, 200)

    def test_category_2_edit(self):
        self.c.login(email='spec@gmail.com', password='1')
        edit_category = models.QuestionCategory.objects.get(name='New Category')
        response = self.c.post(f'/institution/category/{edit_category.id}/edit/', {'new_name': 'NewName'})
        self.assertEqual(response.status_code, 301)

    def test_category_3_delete(self):
        self.c.login(email='spec@gmail.com', password='1')
        del_category = QuestionCategory.objects.get(name='NewName')
        response = self.c.get(f'/institution/category/{del_category.id}/delete/')
        self.assertEqual(response.status_code, 301)
