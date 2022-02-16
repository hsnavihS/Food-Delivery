from django.urls import path
from .views import AddOrderView  # , AllOrdersView, ClearOrderView, CurrentOrderView

urlpatterns = [
    path('add', AddOrderView.as_view(), name="add-order"),
    # path('view', CurrentOrderView.as_view(), name='current-order'),
    # path('viewall', AllOrdersView.as_view(), name='my-orders'),
    # path('clear', ClearOrderView.as_view(), name='clear-cart'),
]
