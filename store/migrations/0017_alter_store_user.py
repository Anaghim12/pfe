# Generated by Django 3.2 on 2022-04-11 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0016_auto_20220411_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='store', to=settings.AUTH_USER_MODEL),
        ),
    ]