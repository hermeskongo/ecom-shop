# Generated by Django 5.1.6 on 2025-02-16 12:42

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'invalid': 'Veuillez entrez un numéro de téléphone valide', 'unique': 'Il existe déjà un utilisateur avec ce numéro'}, max_length=128, null=True, region=None, unique=True),
        ),
    ]
