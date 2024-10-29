# Generated by Django 5.1.1 on 2024-10-27 22:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foods', '0001_initial'),
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foods', to='restaurants.restaurant'),
        ),
        migrations.AddConstraint(
            model_name='food',
            constraint=models.UniqueConstraint(fields=('name', 'restaurant'), name='unique_food_name_per_restaurant'),
        ),
    ]