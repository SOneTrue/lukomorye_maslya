from django.contrib import admin
from .models import Category, Product, Order, OrderItem, ContactRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available", "updated")
    list_filter = ("available", "category")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer_name", "phone", "status", "created_at", "total_items")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "customer_name", "phone")
    inlines = [OrderItemInline]



@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "created_at", "processed")
    list_filter = ("processed", "created_at")
    search_fields = ("name", "phone", "email", "message")
    list_editable = ("processed",)