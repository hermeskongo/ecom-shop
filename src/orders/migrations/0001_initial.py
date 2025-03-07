# Generated by Django 5.1.6 on 2025-02-19 18:02

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(unique=True, verbose_name="Numéro de l'ordre")),
                ('status', models.CharField(choices=[('Nouveau', 'Nouveau'), ('Accepté', 'Accepté'), ('Complété', 'Complété'), ('Annulé', 'Annulé')], default='Nouveau', max_length=25)),
                ('first_name', models.CharField(max_length=155, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=155, verbose_name='Nom')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='E-mail')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(error_messages={'invalid': 'Veuillez entrez un numéro de téléphone valide'}, max_length=128, region=None)),
                ('address', models.CharField(max_length=300, verbose_name='Adresse')),
                ('country', models.CharField(choices=[('Burkina Faso', 'Burkina Faso'), ('Maroc', 'Maroc'), ('France', 'France')], max_length=75, verbose_name='Pays')),
                ('city', models.CharField(choices=[('Ouagadougou', 'Ouagadougou'), ('Bobo Dioulasso', 'Bobo Dioulasso'), ('Casablanca', 'Casablanca'), ('Rabat', 'Rabat'), ('Agadir', 'Agadir'), ('Marrakech', 'Marrakech'), ('Paris', 'Paris'), ('Marseille', 'Marseille'), ('Nice', 'Nice')], max_length=75, verbose_name='Villes')),
                ('total', models.FloatField()),
                ('tax', models.FloatField(verbose_name='Taxe')),
                ('note', models.TextField(blank=True, max_length=250, verbose_name='Note pour la commande')),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('method', models.CharField(choices=[('paypal', 'paypal'), ('wise', 'wise'), ('carte de crédit', 'carte de crédit')], max_length=100, verbose_name='Méthodes de paiements')),
                ('amount', models.FloatField(verbose_name='Montant')),
                ('status', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Paiement',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50, verbose_name='Couleur')),
                ('size', models.CharField(max_length=50, verbose_name='Taille')),
                ('quantity', models.IntegerField(verbose_name='Quantité')),
                ('product_price', models.FloatField(verbose_name='Prix du produit')),
                ('is_ordered', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.productvariations')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment'),
        ),
    ]
