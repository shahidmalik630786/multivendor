# Generated by Django 5.2 on 2025-06-06 13:30

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_userprofile_address_alter_userprofile_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
