from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from .serializers import CustomerSerializer, RestaurantSerializer
from .permissions import IsLoggedIn
from rest_framework.generics import CreateAPIView
from .utils import get_user
from orders.models import Dish
from orders.serializers import DishSerializer


class CustomerRegisterView(CreateAPIView):

    '''
    View for registering a customer
    Accepted method: POST
    URI: /user/customer/register
    '''

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RestaurantRegisterView(CreateAPIView):

    '''
    View for registering a restaurant
    Accepted method: POST
    URI: /user/restaurant/register
    '''

    def post(self, request):
        data = request.data
        serializer = RestaurantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant = serializer.save()
        if data.get('menu'):
            for item in data.get('menu'):
                if item.get('id'):
                    dish = Dish.objects.get(id=int(item['id']))
                    restaurant.menu.add(dish)
                else:
                    dish_serializer = DishSerializer(data=item)
                    dish_serializer.is_valid(raise_exception=True)
                    dish = dish_serializer.save()
                    restaurant.menu.add(dish)
            restaurant.save()
        return Response(serializer.data)


class LoginView(APIView):

    '''
    View for logging a user in
    Accepted method: POST
    URI: /user/login
    '''

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if email is None or password is None:
            message = {"Invalid": "Email and / or password not provided."}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(email=email, password=password)

        response = Response()

        if user is not None:
            refresh_token = RefreshToken.for_user(user)
            response.set_cookie(
                key=settings.SIMPLE_JWT['COOKIE_KEY'],
                value=str(user.id),
                expires=settings.SIMPLE_JWT['COOKIE_EXPIRES'],
                secure=settings.SIMPLE_JWT['COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['COOKIE_SAMESITE']
            )
            request.session['access_token'] = str(refresh_token.access_token)
            response.data = {
                "Message": "Login successful!"
            }
            return response
        else:
            message = {"Invalid": "User with the given credentials not found."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):

    '''
    View for getting details about a user
    Accepted method: GET
    URI: /user
    '''

    permission_classes = [IsLoggedIn]

    def get(self, request):
        user = get_user(request)
        if user.is_restaurant:
            serializer = RestaurantSerializer(user, many=False)
            return Response(serializer.data)
        else:
            serializer = CustomerSerializer(user, many=False)
            return Response(serializer.data)


class LogoutView(APIView):

    '''
    View for logging out a user
    Accepted method: POST
    URI: /user/logout
    '''

    permission_classes = [IsLoggedIn]

    def post(self, request):
        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT['COOKIE_KEY'])
        if request.session.get('access_token') is not None:
            del request.session['access_token']
        response.data = {"Message": "Logged out successfully"}
        return response


class UserUpdateView(APIView):

    '''
    View to update a user's details
    Accepted methods: PATCH
    URI: /user/update
    '''

    permission_classes = [IsLoggedIn]

    def patch(self, request):
        response = Response()
        user = get_user(request)

        if request.data.get('email') or request.data.get('is_restaurant') or request.data.get('is_customer') or request.data.get('password'):
            response.status_code = status.HTTP_400_BAD_REQUEST
            response.data = {
                "detail": "One or more of the passed fields cannot be updated"}
            return response

        if user.is_customer:
            serializer = CustomerSerializer(
                user, data=request.data, partial=True)
        else:
            serializer = RestaurantSerializer(
                user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response.status_code = status.HTTP_202_ACCEPTED
            response.data = serializer.data
            return response
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.data = serializer.errors
        return response


class UserDeleteView(APIView):

    '''
    View to delete a user's account
    Accepted method: DELETE
    URI: /user/delete
    '''

    permission_classes = [IsLoggedIn]

    def delete(self, request):
        user = get_user(request)
        user.delete()
        response = Response()
        response.delete_cookie(settings.SIMPLE_JWT['COOKIE_KEY'])
        if request.session.get('access_token') is not None:
            del request.session['access_token']
        response.data = {"details": "Deleted user successfully"}
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
