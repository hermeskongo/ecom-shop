# Generated by Django 5.1.6 on 2025-02-14 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_productvariations_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariations',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='store.products', verbose_name='Produit'),
        ),
    ]
