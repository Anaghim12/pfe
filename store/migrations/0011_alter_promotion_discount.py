# Generated by Django 3.2 on 2022-03-31 10:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_promotion_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
