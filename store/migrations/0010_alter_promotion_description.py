# Generated by Django 3.2 on 2022-03-31 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20220331_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='description',
            field=models.CharField(max_length=15),
        ),
    ]