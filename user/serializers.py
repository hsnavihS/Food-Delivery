from rest_framework import serializers
from .models import CustomUser


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'is_customer']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        validated_data['is_customer'] = True
        validated_data['is_restaurant'] = False
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'is_restaurant']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        validated_data['is_customer'] = False
        validated_data['is_restaurant'] = True
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
