from rest_framework import serializers
from .models import CustomUser


class CustomerSerializer(serializers.ModelSerializer):

    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password',
                  'is_customer', 'address', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_profile_picture(self, obj):
        if obj.picture is not None:
            profile_picture = obj.picture.url
            return profile_picture
        else:
            return None

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

    restaurant_image = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password',
                  'is_restaurant', 'address', 'restaurant_image']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_restaurant_image(self, obj):
        if obj.picture is not None:
            restaurant_image = obj.picture.url
            return restaurant_image
        else:
            return None

    def create(self, validated_data):

        password = validated_data.pop('password', None)
        validated_data['is_customer'] = False
        validated_data['is_restaurant'] = True
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
