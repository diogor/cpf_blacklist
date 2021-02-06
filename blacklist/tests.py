from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from blacklist.models import ListEntry


class APITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.test_user = User.objects.create_user(
            "testuser", "test@test.com", "testpass"
        ) 
        self.test_user.user_permissions.add(
            Permission.objects.get(
                codename='add_listentry',
                content_type=ContentType.objects.get_for_model(ListEntry))
        )
        self.auth_url = reverse('token_obtain_pair')
        self.url = reverse('listentry-list')
        self.valid_data = {'cpf': '24637583098'}
        self.valid_data1 = {'cpf': '12107074038'}
        self.invalid_data1 = {'cpf': '00494995'}
        self.invalid_data2 = {'cpf': '09876563746'}
        self.invalid_data3 = {'cpf': 'abeudjksiye'}
        self.valid_user = {
            "username": "testuser",
            "password": "testpass"
        }
        self.invalid_user = {
            "username": "t",
            "password": "s"
        }
        ListEntry.objects.create(**self.valid_data1)

    def test_create_unauthenticated(self):
        # no token
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('detail' in response.data.keys())

        # invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer Token')
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("token_not_valid", response.data.get('code'))

    def test_authentication(self):
        # valid credentials
        response = self.client.post(self.auth_url, self.valid_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data.keys())

        # invalid credentials
        response = self.client.post(self.auth_url, self.invalid_user)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('detail' in response.data.keys())

    def test_create_authenticated(self):
        response = self.client.post(self.auth_url, self.valid_user)

        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # valid cpf
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # invalid cpf
        response = self.client.post(self.url, self.invalid_data1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, self.invalid_data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, self.invalid_data3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_cpf(self):
        # not in list
        response = self.client.get(reverse('listentry-detail',
                                           kwargs={"cpf": self.valid_data["cpf"]}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ListEntry.STATUS_ALLOW, response.data['status'])

        # in list
        response = self.client.get(
            reverse('listentry-detail', kwargs={"cpf": self.valid_data1["cpf"]}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ListEntry.STATUS_DENY, response.data['status'])

        # invalid
        response = self.client.get(
            reverse('listentry-detail', kwargs={"cpf": self.invalid_data1["cpf"]}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('detail' in response.data.keys())
