# Generated by Django 3.2 on 2022-04-15 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0020_auto_20220415_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='id',
        ),
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='store', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
