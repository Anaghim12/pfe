# Generated by Django 3.2 on 2022-03-09 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='type',
        ),
    ]
