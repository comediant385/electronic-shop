from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Category(models.Model):
    category_name = models.CharField(
        max_length=150,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории",
    )
    category_description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        **NULLABLE,
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    objects = None
    product_name = models.CharField(
        max_length=150,
        verbose_name="Наименование продукта",
        help_text="Введите наименование продукта",
    )
    product_description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание продукта",
        **NULLABLE,
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение (превью)",
        help_text="Загрузите изображение продукта",
        **NULLABLE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию",
        **NULLABLE,
        related_name="products",
    )
    price = models.IntegerField(
        verbose_name="Цена за покупку",
        help_text="Введите цену за покупку",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания (записи в БД)",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения (записи в БД)",
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Создан пользователем", **NULLABLE,
    )
    published = models.BooleanField(default=False, verbose_name="Опубликован",)

    manufactured_at = models.DateTimeField(
        verbose_name="Дата производства продукта",
        **NULLABLE,
    )

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["product_name", "category"]
        permissions = [
            ('can_cancel_puplication', 'Может отменять публикацию'),
            ('can_change_desription', 'Может менять описание'),
            ('can_change_category', 'Может менять категорию')
        ]


class Version(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="versions"
    )
    version_number = models.PositiveIntegerField(verbose_name="Номер версии")
    version_name = models.CharField(max_length=150, verbose_name="Наименование версии")
    version_current_sign = models.BooleanField(
        default=False, verbose_name="Признак текущей версии"
    )

    def __str__(self):
        return f"{self.version_name} ({self.version_number})"

    class Meta:
        verbose_name = "версия продукта"
        verbose_name_plural = "версии продуктов"
        ordering = ["product", "version_number"]
