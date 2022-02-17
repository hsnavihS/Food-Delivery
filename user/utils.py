from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import CustomUser


def get_user(request):
    user_id = request.COOKIES.get(settings.SIMPLE_JWT['COOKIE_KEY'])
    user = get_object_or_404(CustomUser, id=user_id)
    return user
