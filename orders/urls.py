from django.urls import path
# , AllOrdersView, ClearOrderView, CurrentOrderView
from .views import AcceptOrderView, AddOrderView, CompleteOrderView

urlpatterns = [
    path('add', AddOrderView.as_view(), name="add-order"),
    path('accept', AcceptOrderView.as_view(), name="accept-order"),
    path('complete', CompleteOrderView.as_view(), name="complete-order"),
]
