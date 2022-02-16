from django.shortcuts import render
# AddOrderView, AllOrdersView, ClearOrderView, CurrentOrderView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from user.serializers import CustomUserSerializer
from user.permissions import IsCustomer, IsLoggedIn
from user.models import CustomUser
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from .models import Dish, Order
from django.shortcuts import get_object_or_404


class AddOrderView(CreateAPIView):

    permission_classes = [IsLoggedIn, IsCustomer]

    def post(self, request):

        data = request.data
        response = Response()

        user = data.get('user')
        if user is None:
            response.data = {
                "Error": "User details not provided"}
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response
        else:
            customer_id = user.get('customer')
            restaurant_id = user.get('restaurant')
            if customer_id is None or restaurant_id is None:
                response.data = {
                    "Error": "Both a customer and restaurant account must be affiliated with an order"}
                response.status_code = status.HTTP_400_BAD_REQUEST
                return response
            else:

                customer = get_object_or_404(
                    CustomUser, id=int(customer_id))
                restaurant = get_object_or_404(
                    CustomUser, id=int(restaurant_id))

                if not restaurant.is_restaurant:
                    response.data = {"Error": "Incorrect restaurant details"}
                    response.status_code = status.HTTP_400_BAD_REQUEST
                    return response

                order = Order.objects.create(
                    customer=customer, restaurant=restaurant)

        items = data.get('items')
        if items is None:
            response.data = {
                "Error": "Details about dishes not provided"}
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response
        else:
            order.price = 0
            for id in items:
                dish = Dish.objects.get(id=int(id))
                order.items.add(dish)
                order.price += float(dish.price)

        order.save()
        response.data = {
            "Detail": f"Created order for user {str(customer)} successfully!"}
        return response


# class AllOrdersView(ListAPIView):

#     permission_classes = [IsLoggedIn]

#     def get(self, request):
#         pass
        # queryset = Anime.objects.all()
        # serializer_class = AnimeDetailSerializer
