# Generated by Django 3.2 on 2022-04-04 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_rename_quantity_product_inventory'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
    ]