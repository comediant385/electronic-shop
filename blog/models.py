from django.db import models

NULLABLE = {"blank": True, "null": True}


class BlogPost(models.Model):
    """A blog post"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(max_length=200, unique=True, verbose_name="Slug", **NULLABLE)
    body = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(verbose_name="Превью", upload_to="blog/", **NULLABLE)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    published = models.BooleanField(verbose_name="Признак публикации", default=True)
    views = models.PositiveIntegerField(verbose_name="Количество просмотров", editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"