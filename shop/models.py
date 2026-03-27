from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    icon  = models.CharField("Bootstrap-иконка", max_length=50,
                              default="bi-box", blank=True)  # например "bi-balloon"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:catalog_by_category", args=[self.slug])


class Product(models.Model):
    category    = models.ForeignKey(
        Category, related_name="products",
        on_delete=models.CASCADE, verbose_name="Категория",
    )
    name        = models.CharField("Название", max_length=200)
    slug        = models.SlugField(max_length=220, unique=True)
    description = models.TextField("Описание", blank=True)
    price       = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    old_price   = models.DecimalField("Старая цена", max_digits=10,
                                       decimal_places=2, blank=True, null=True)
    available   = models.BooleanField("В наличии", default=True)
    is_hit      = models.BooleanField("Хит продаж", default=False)
    image       = models.ImageField("Изображение", upload_to="products/",
                                     blank=True, null=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Игрушка"
        verbose_name_plural = "Игрушки"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.id, self.slug])

    @property
    def discount_percent(self):
        """Процент скидки относительно old_price."""
        if self.old_price and self.old_price > self.price:
            return round((1 - self.price / self.old_price) * 100)
        return None

    @property
    def image_url(self):
        """Безопасное получение URL картинки."""
        if self.image:
            return self.image.url
        return "/static/img/no-image.png"