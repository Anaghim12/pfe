# Generated by Django 3.2 on 2022-05-29 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0050_auto_20220528_0216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demanderetour',
            name='image_facture',
        ),
        migrations.RemoveField(
            model_name='demanderetour',
            name='image_produit',
        ),
    ]
