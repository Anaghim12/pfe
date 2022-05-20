# Generated by Django 3.2 on 2022-05-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_alter_aprod_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='subcollection',
            options={'ordering': ['collection_id']},
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]