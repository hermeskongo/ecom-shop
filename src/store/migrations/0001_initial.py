# Generated by Django 5.1.6 on 2025-02-12 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155, unique=True, verbose_name='Nom de la catégorie')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(max_length=500)),
            ],
            options={
                'verbose_name': 'Catégories',
            },
        ),
    ]
