import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Category, Product, Order, OrderItem, ContactRequest


def index(request):
    categories = Category.objects.all()
    popular_products = Product.objects.filter(available=True, is_hit=True)[:4]

    if not popular_products.exists():
        popular_products = Product.objects.filter(available=True)[:4]

    return render(request, "store/index.html", {
        "categories": categories,
        "popular_products": popular_products,
    })


def product_list(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by("-id")

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    paginator = Paginator(products, 9)  # 9 товаров на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "store/product_list.html", {
        "current_category": current_category,
        "categories": categories,
        "products": page_obj,
        "page_obj": page_obj,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    return render(request, "store/product_detail.html", {
        "product": product,
        "related_products": related_products,
    })


def cart_page(request):
    return render(request, "store/cart.html")


@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)

        customer_name = data.get("customer_name", "").strip()
        phone = data.get("phone", "").strip()
        comment = data.get("comment", "").strip()
        items = data.get("items", [])

        if not customer_name or not phone:
            return JsonResponse({
                "success": False,
                "message": "Укажите имя и телефон."
            }, status=400)

        if not items:
            return JsonResponse({
                "success": False,
                "message": "Корзина пуста."
            }, status=400)

        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            comment=comment,
            status="new"
        )

        for item in items:
            product_id = item.get("id")
            quantity = int(item.get("quantity", 1))

            product = get_object_or_404(Product, id=product_id, available=True)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        return JsonResponse({
            "success": True,
            "order_number": order.order_number,
            "message": f"Заказ оформлен. Номер заказа: {order.order_number}"
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"Ошибка оформления заказа: {str(e)}"
        }, status=400)

def submit_contact_request(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if name and phone:
            ContactRequest.objects.create(
                name=name,
                phone=phone,
                email=email,
                message=message
            )
            messages.success(request, "✅ Ваш вопрос успешно отправлен! Мы свяжемся с вами.")
        else:
            messages.error(request, "⚠️ Пожалуйста, заполните имя и телефон.")

        return redirect("store:index")

    return redirect("store:index")

def privacy_policy(request):
    return render(request, "store/privacy_policy.html")


def user_agreement(request):
    return render(request, "store/user_agreement.html")