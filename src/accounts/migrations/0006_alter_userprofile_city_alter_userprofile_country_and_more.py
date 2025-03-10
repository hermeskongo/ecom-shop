# Generated by Django 5.1.6 on 2025-02-23 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, choices=[('Ouagadougou', 'Ouagadougou'), ('Bobo Dioulasso', 'Bobo Dioulasso'), ('Casablanca', 'Casablanca'), ('Rabat', 'Rabat'), ('Agadir', 'Agadir'), ('Marrakech', 'Marrakech'), ('Paris', 'Paris'), ('Marseille', 'Marseille'), ('Nice', 'Nice')], max_length=50, verbose_name='Ville'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, choices=[('Burkina Faso', 'Burkina Faso'), ('Maroc', 'Maroc'), ('France', 'France')], max_length=50, verbose_name='Pays'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile', verbose_name='Photo de profile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='quartier',
            field=models.CharField(blank=True, max_length=70, verbose_name='Quartier'),
        ),
    ]
