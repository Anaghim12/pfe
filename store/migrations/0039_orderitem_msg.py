# Generated by Django 3.2 on 2022-05-05 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_auto_20220505_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='msg',
            field=models.CharField(default='', max_length=255),
        ),
    ]
