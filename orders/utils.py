from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order


def get_order_by_id(request):
    order_id = request.data.get("id")
    response = Response()
    if order_id is None:
        response.data = {"detail": "No order ID provided"}
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    order = get_object_or_404(Order, unique_id=int(order_id))
    return order
