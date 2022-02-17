import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # TODO: Add image field
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Dishes'


class Order(models.Model):
    ordered_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    items = models.ManyToManyField(
        'Dish', related_name='order', blank=True)
    is_accepted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    customer = models.ForeignKey(
        User, related_name='placed_orders', on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(
        User, related_name='received_orders', on_delete=models.CASCADE, null=True, blank=True)
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f'Order: placed on {self.ordered_on.strftime("%b %d, %I:%M %p")}'
