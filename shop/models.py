from django.db import models

class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    available = models.BooleanField("В наличии", default=True)
    image = models.ImageField("Изображение", upload_to="products/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Игрушка"
        verbose_name_plural = "Игрушки"
        ordering = ["name"]

    def __str__(self):
        return self.name
