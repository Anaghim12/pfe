# Generated by Django 3.2 on 2022-04-01 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_promotion_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantity',
            new_name='inventory',
        ),
    ]
