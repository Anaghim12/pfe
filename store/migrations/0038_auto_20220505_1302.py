# Generated by Django 3.2 on 2022-05-05 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_order_msg'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='display',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='msg',
            field=models.CharField(default='', max_length=255),
        ),
    ]