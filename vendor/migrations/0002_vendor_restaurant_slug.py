# Generated by Django 5.1.6 on 2025-02-20 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='restaurant_slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
