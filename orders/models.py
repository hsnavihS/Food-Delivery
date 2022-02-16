from django.db.models.signals import post_save
from django.dispatch import receiver
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
        User, related_name='placed_orders', on_delete=models.CASCADE, null=False, blank=False)
    restaurant = models.ForeignKey(
        User, related_name='received_orders', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f'Order: placed on {self.ordered_on.strftime("%b %d, %I:%M %p")}'


# TODO: calculate total price of an order using a view or a signal
# @receiver(post_save, sender=Order)
# def my_callback(sender, instance, update_fields, *args, **kwargs):
#     if update_fields is None:
#         price = 0
#         for item in instance.items.all():
#             price += float(item.price)
#         instance.price = price
#         instance.save(update_fields=['price'])
