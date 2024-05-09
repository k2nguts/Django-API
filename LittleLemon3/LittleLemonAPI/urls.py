from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path ('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
    path('category/',views.CategoryItemView.as_view()),
    path('menu/',views.menu),
    path('menu-items',views.MenuItem),
    path('welcome',views.welcome),
    path('secret',views.secret),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view',views.manager_view),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
    path('groups/manager/users',views.managers),
    path('ratings', views.RatingsView.as_view()),
    path ('menu-items/all', views.MenuItemViewAll.as_view()),
    path('cart/menu-items',views.CartView.as_view()),
    ]