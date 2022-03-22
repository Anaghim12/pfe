# Generated by Django 3.2 on 2022-03-18 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.type'),
        ),
    ]