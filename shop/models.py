from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(
        "Bootstrap-иконка",
        max_length=50,
        default="bi-box",
        blank=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:catalog_by_category", args=[self.slug])


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
    old_price = models.DecimalField(
        "Старая цена",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    available = models.BooleanField("В наличии", default=True)
    is_hit = models.BooleanField("Хит продаж", default=False)
    image = models.ImageField(
        "Изображение",
        upload_to="products/",
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
        if self.old_price and self.old_price > self.price:
            return round((1 - self.price / self.old_price) * 100)
        return None

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/img/no-image.png"


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("assembling", "Собирается"),
        ("ready", "Готов к выдаче"),
        ("done", "Выдан"),
        ("cancelled", "Отменён"),
    ]

    order_number = models.CharField("Номер заказа", max_length=30, unique=True)
    customer_name = models.CharField("Имя клиента", max_length=255)
    phone = models.CharField("Телефон", max_length=30)
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} — {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            now = timezone.localtime()
            unique_part = str(uuid.uuid4().int)[:4]
            self.order_number = f"LK-{now.strftime('%Y%m%d')}-{unique_part}"
        super().save(*args, **kwargs)

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена на момент заказа", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"