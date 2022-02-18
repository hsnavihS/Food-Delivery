from django.urls import path
from .views import CustomerRegisterView, LoginView, LogoutView, RestaurantRegisterView, UserView, UserUpdateView, UserDeleteView, AllOrdersView

urlpatterns = [
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name='logout'),
    path('customer/register', CustomerRegisterView.as_view(),
         name='register-customer'),
    path('restaurant/register', RestaurantRegisterView.as_view(),
         name='register-restaurant'),
    path('update',
         UserUpdateView.as_view(), name='update-user'),
    path('delete',
         UserDeleteView.as_view(), name='delete-user'),
    path('allorders', AllOrdersView.as_view(), name='all-orders'),
    path('', UserView.as_view(), name='get-user'),
]
