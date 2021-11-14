from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexListView.as_view(), name='top'),  # トップページ
    # path('', views.index),

    # Account
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='sign_up'),
    path('account/', views.AccountUpdateView.as_view(), name='account'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),

    # Items
    path('items/<str:pk>/', views.ItemDetailView.as_view(), name='item'),
    path('categories/<str:pk>/', views.CategoryListView.as_view(), name='category_list'),
    path('tags/<str:pk>/', views.TagListView.as_view(), name='tag_list'),

    # Cart
    path('cart/', views.CartListView.as_view(), name='cart_list'),
    path('cart/add/', views.AddCartView.as_view(), name='add_cart'),
    path('cart/remove/<str:pk>/', views.remove_from_cart, name='remove_cart'),

    # Pay
    path('pay/checkout/', views.PayWithStripe.as_view(), name='pay'),
    path('pay/success/', views.PaySuccessView.as_view(), name='success_pay'),
    path('pay/cancel/', views.PayCancelView.as_view(), name='cancel_pay'),

    # Order
    path('orders/', views.OrderIndexView.as_view(), name='order_list'),
    path('orders/<str:pk>/', views.OrderDetailView.as_view(), name='order'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
