# Generated by Django 5.1.1 on 2024-10-29 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='menu',
            name='unique_menu_per_date_per_restaurant',
        ),
    ]
