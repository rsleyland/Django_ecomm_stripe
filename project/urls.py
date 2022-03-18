from django.contrib import admin
from django.urls.conf import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Products.views import product_detail, product_all
from Order.views import get_order as order_detail_id
from Account.views import register, profile, confirm_code, delete_acc, update_email, update_password
from Carts.views import cart, remove_from_cart, update_cart, empty_cart, add_to_cart, create_checkout_session, my_webhook, cart_success, cart_cancel, pre_checkout

urlpatterns = [
    path('', profile, name='profile'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register'),
    path('accounts/delete/', delete_acc, name='delete'),
    path('accounts/update_email/', update_email, name='update_email'),
    path('accounts/update_password/', update_password, name='update_password'),
    path('accounts/email-confirmation/', confirm_code, name='confirm_code'),
    path('cart/', cart, name='cart'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<product_name>', remove_from_cart, name='cart_remove'),
    path('cart/update/', update_cart, name='cart_update'),
    path('cart/empty/', empty_cart, name='cart_empty'),
    path('cart/cancel/', cart_cancel, name='cart_cancel'),
    path('cart/success/', cart_success, name='cart_success'),
    path('cart/pre-checkout/', pre_checkout, name='pre_checkout'),
    path('create-checkout-session/', create_checkout_session, name='checkout'),
    path('order/all', order_detail_id),
    path('order/<int:pk>', order_detail_id),
    path('profile/', profile, name='profile'),
    path('products/', product_all, name='products'),
    path('products/<prod_name>/', product_detail, name='product_detail'),
    path('webhook', my_webhook),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
