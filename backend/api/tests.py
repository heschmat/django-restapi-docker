from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from .models import User, Order


class UserOrderAPITestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', password='ch@ngeM3!')
        self.user2 = User.objects.create_user(username='test2', password='changeM3!')

        Order.objects.create(user=self.user1)
        Order.objects.create(user=self.user1, status='CONFIRMED')
        Order.objects.create(user=self.user2)

    def test_user_orders_authenticated_user_sees_only_their_orders(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('user-orders'))
        orders = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(order['user'] == self.user2.id for order in orders))

    def test_user_orders_unauthenticated_user_gets_401(self):
        """
        When the permission checks fail, either of the followings is sent as response:
        either "403 Forbidden" or "401 Unauthorized"
        As JWT is top of the authentication list (in settings.py), 401 will be sent.
        """
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_orders_does_not_include_others_orders(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('user-orders'))
        orders = response.json()

        user_ids = {order['user'] for order in orders}
        self.assertEqual(user_ids, {self.user1.id})
