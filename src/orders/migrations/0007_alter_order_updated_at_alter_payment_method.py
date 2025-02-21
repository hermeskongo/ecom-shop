# Generated by Django 5.1.6 on 2025-02-20 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_created_at_alter_order_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Date de modification'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('paypal', 'paypal'), ('wise', 'wise'), ('paytest', 'paytest'), ('carte de crédit', 'carte de crédit')], max_length=100, verbose_name='Méthodes de paiements'),
        ),
    ]
