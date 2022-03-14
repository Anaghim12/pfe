# Generated by Django 3.2 on 2022-03-09 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.type'),
        ),
    ]