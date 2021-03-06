# Generated by Django 3.2 on 2022-03-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_storeitemwishlist_storewishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='membership',
            field=models.CharField(blank=True, choices=[('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold')], default='B', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='order_count',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
