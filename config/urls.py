from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.IndexListView.as_view()),  # トップページ
    # path('', views.index),

    # Account
    path('login/', views.Login.as_view(), ),
    path('logout/', LogoutView.as_view(), ),
    path('signup/', views.SignUpView.as_view(), ),
    path('account/', views.AccountUpdateView.as_view(), ),
    path('profile/', views.ProfileUpdateView.as_view(), ),

    # Items
    path('items/<str:pk>/', views.ItemDetailView.as_view()),
    path('categories/<str:pk>/', views.CategoryListView.as_view(), ),
    path('tags/<str:pk>/', views.TagListView.as_view(),),

    # Cart
    path('cart/', views.CartListView.as_view(),),
    path('cart/add/', views.AddCartView.as_view(),),
    path('cart/remove/<str:pk>/', views.remove_from_cart,),

    # Pay
    path('pay/checkout/', views.PayWithStripe.as_view(),),
    path('pay/success/', views.PaySuccessView.as_view(),),
    path('pay/cancel/', views.PayCancelView.as_view(),),

    # Order
    path('orders/', views.OrderIndexView.as_view(), ),
    path('orders/<str:pk>/', views.OrderDetailView.as_view(), ),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
