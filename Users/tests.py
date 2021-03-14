import json

from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestUser(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.count = self.User.objects.count()
        self.password = 'admin'
        self.user = self.User.objects.create_user(username='user', email='user@gmail.com',
                                                  password=self.password, is_upgraded=True)
        self.admin_user = self.User.objects.create_superuser(username='admin', email='admin@gmail.com',
                                                             password=self.password, is_upgraded=True)
        self.client = APIClient()

    def test_valid_list_user(self):
        self.assertEqual(self.count + 2, self.User.objects.count())
        self.client.force_login(self.admin_user)

        url_list = reverse('user_list')
        response = self.client.get(url_list)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.client.force_login(self.user)
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_list_user(self):
        url_list = reverse('user_list')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_login_user(self):
        url_login = reverse('user_login')
        data = {
            'email': 'user@gmail.com',
            'password': self.password
        }
        data1 = json.dumps(data)
        response = self.client.post(url_login, data1, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_invalid_login_user(self):
        url_login = reverse('user_login')
        data = json.dumps({
            'email': 'user@gmail.com'})
        response = self.client.post(url_login, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestProfile(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='user', email='user@gmail.com',
                                                  password='rootroot', is_upgraded=True)
        self.admin_user = self.User.objects.create_superuser(username='admin', email='admin@gmail.com',
                                                             password='adminadmin', is_upgraded=True)
        self.client = APIClient()

    def test_valid_create_profile(self):
        url_create = reverse('create_profile')
        data = {
            'first_name': 'name',
            'last_name': 'surname',
            'about': 'about',
            'birthday': '2020-11-11',
            'gender': 'M',
            'owner': self.admin_user.id
        }
        data1 = json.dumps(data)
        self.client.force_login(self.admin_user)
        response = self.client.post(url_create, data1, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertEqual(response.data['birthday'], data['birthday'])

    def test_invalid_create_profile(self):
        url_create = reverse('create_profile')
        data = {
            'first_name': 'name',
            'last_name': 'surname',
            'about': 'about',
            'birthday': '2020-11-11',
            'owner': self.admin_user.id
        }
        data1 = json.dumps(data)
        self.client.force_login(self.admin_user)
        response = self.client.post(url_create, data1, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_valid_list_profile(self):
        url_list = reverse('list_profile')
        self.client.force_login(self.admin_user)
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_list_profile(self):
        url_list = reverse('list_profile')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_login(self.user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
