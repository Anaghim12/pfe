# Generated by Django 3.2 on 2022-03-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220323_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='role',
            field=models.CharField(default='1', max_length=255),
        ),
    ]
