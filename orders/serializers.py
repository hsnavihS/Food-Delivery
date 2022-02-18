from rest_framework import serializers
from .models import Dish, Order


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = ['name', 'description', 'price']


class OrderSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    unique_id = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['unique_id', 'ordered_on', 'price', 'is_accepted',
                  'is_completed', 'customer', 'restaurant', 'items']

    def get_items(self, obj):
        items = obj.items.all()
        res = [{
            "name": item.name,
            "description": item.description,
            "price": item.price
        }
            for item in items]
        return res

    def get_customer(self, obj):
        return {
            "id": obj.customer.id,
            "email": obj.customer.email,
            "name": obj.customer.username
        }

    def get_restaurant(self, obj):
        return {
            "id": obj.restaurant.id,
            "email": obj.restaurant.email,
            "name": obj.restaurant.username
        }

    def get_unique_id(self, obj):
        return int(obj.unique_id)
