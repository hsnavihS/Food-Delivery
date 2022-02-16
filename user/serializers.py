from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password',
                  'is_restaurant', 'is_customer']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):

        # to ensure that the user is either a restaurant or a customer
        is_restaurant = validated_data.pop('is_restaurant', None)
        is_customer = validated_data.pop('is_customer', None)
        if is_restaurant is False and is_customer is False:
            raise serializers.ValidationError(
                {"detail": "User must be either a customer or a restaurant"})
        elif is_restaurant is True and is_customer is True:
            raise serializers.ValidationError(
                {"detail": "User can either be a customer or a restaurant, not both"})

        # to ensure that password is set in a hashed format, not as a raw string
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
