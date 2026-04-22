from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.index, name="index"),
    path("catalog/", views.product_list, name="catalog"),
    path("catalog/<slug:category_slug>/", views.product_list, name="catalog_by_category"),
    path("basket/", views.cart_page, name="cart"),
    path("order/create/", views.create_order, name="create_order"),
    path("<int:id>/<slug:slug>/", views.product_detail, name="product_detail"),
    path("contact/submit/", views.submit_contact_request, name="submit_contact_request"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("user-agreement/", views.user_agreement, name="user_agreement"),
]