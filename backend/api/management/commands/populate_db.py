import os
import random
import csv

from django.core.management.base import BaseCommand
# from django.utils import lorem_ipsum
from api.models import User, Product, Order, OrderItem


class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **kwargs):
        # get or create superuser
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='changeME!')

        # create products - name, desc, price, stock, image
        products = []

        # Open the CSV file
        csv_path = os.path.join(os.path.dirname(__file__), 'products_db.csv')
        with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Iterate through each row (as a dictionary)
            for row in reader:
                products.append(Product(**row))

        # create products & re-fetch from DB
        Product.objects.bulk_create(products)
        products = Product.objects.all()

        # create some dummy orders tied to the superuser
        for _ in range(5):
            # create an Order with 2 order items
            order = Order.objects.create(user=user)
            for product in random.sample(list(products), 2):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1, 3)
                )
