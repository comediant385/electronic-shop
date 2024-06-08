import json

from django.core.management import BaseCommand
from django.db import connection

from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_catalog():
        with open("catalog_data.json", encoding="UTF-8") as file:
            return json.load(file)

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;")

        Category.objects.all().delete()
        Product.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_catalog():
            if category["model"] == "catalog.category":
                category_for_create.append(
                    Category(
                        category_name=category["fields"]["category_name"],
                        category_description=category["fields"]["category_description"],
                    )
                )

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_catalog():
            if product["model"] == "catalog.product":
                product_for_create.append(
                    Product(
                        product_name=product["fields"]["product_name"],
                        product_description=product["fields"]["product_description"],
                        category=Category.objects.get(pk=product["fields"]["category"]),
                        price=product["fields"]["price"],
                    )
                )
        Product.objects.bulk_create(product_for_create)
