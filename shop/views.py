from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def index(request):
    categories = Category.objects.all()
    popular_products = Product.objects.filter(available=True, is_hit=True)[:4]
    # Если хитов нет — показываем любые 4
    if not popular_products.exists():
        popular_products = Product.objects.filter(available=True)[:4]
    return render(request, "store/index.html", {
        "categories": categories,
        "popular_products": popular_products,
    })


def product_list(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    return render(request, "store/product_list.html", {
        "current_category": current_category,
        "categories": categories,
        "products": products,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]
    return render(request, "store/product_detail.html", {
        "product": product,
        "related_products": related_products,
    })