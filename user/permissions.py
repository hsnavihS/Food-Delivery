from rest_framework import permissions
from rest_framework_simplejwt.tokens import AccessToken
from user.utils import get_user
from .models import CustomUser
from django.conf import settings


class IsLoggedIn(permissions.BasePermission):
    message = 'User needs to be logged in'

    def has_permission(self, request, view):
        user_id = request.COOKIES.get(settings.SIMPLE_JWT['COOKIE_KEY'], None)
        token = request.session.get('access_token')
        if user_id is None:
            return False
        token_object = AccessToken(token)
        return int(user_id) == int(token_object['user_id'])


class IsAdmin(permissions.BasePermission):
    message = 'User needs to be an admin'

    def has_permission(self, request, view):
        user_id = request.COOKIES.get(settings.SIMPLE_JWT['COOKIE_KEY'], None)
        if user_id is not None:
            user = CustomUser.objects.get(id=user_id)
            return user.is_superuser
        return False


class IsRestaurant(permissions.BasePermission):
    message = 'User needs to be a restaurant'

    def has_permission(self, request, view):
        user = get_user(request)
        if type(user) == CustomUser:
            return user.is_restaurant
        else:
            return False


class IsCustomer(permissions.BasePermission):
    message = 'User needs to be a customer'

    def has_permission(self, request, view):
        user = get_user(request)
        if type(user) == CustomUser:
            return user.is_customer
        else:
            return False
