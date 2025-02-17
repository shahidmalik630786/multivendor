# Generated by Django 5.1.6 on 2025-02-13 08:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_alter_vendor_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_license',
            field=models.ImageField(upload_to='vendor/license', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])]),
        ),
    ]
