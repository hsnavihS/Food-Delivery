# Generated by Django 4.0.1 on 2022-02-17 15:16

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0004_order_unique_id_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='placed_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
