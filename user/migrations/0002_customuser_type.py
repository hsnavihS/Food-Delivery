# Generated by Django 4.0.1 on 2022-02-16 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='type',
            field=models.CharField(choices=[('CU', 'Customer'), ('RE', 'Restaurant')], default='CU', max_length=2),
        ),
    ]
