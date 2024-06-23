# Generated by Django 5.0.4 on 2024-05-13 13:57
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Version",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "version_number",
                    models.PositiveIntegerField(verbose_name="Номер версии"),
                ),
                (
                    "version_name",
                    models.CharField(
                        max_length=150, verbose_name="Наименование версии"
                    ),
                ),
                (
                    "version_current_sign",
                    models.BooleanField(
                        default=False, verbose_name="Признак текущей версии"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="versions",
                        to="catalog.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "версия продукта",
                "verbose_name_plural": "версии продуктов",
                "ordering": ["product", "version_number"],
            },
        ),
    ]
