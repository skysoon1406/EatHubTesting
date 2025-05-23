# Generated by Django 4.2.20 on 2025-05-09 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_remove_restaurant_url_alter_review_rating'),
        ('users', '0002_user_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='merchant_user', to='restaurants.restaurant'),
        ),
    ]
