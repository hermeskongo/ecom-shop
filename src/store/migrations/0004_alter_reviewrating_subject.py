# Generated by Django 5.1.6 on 2025-02-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_reviewrating_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='subject',
            field=models.CharField(max_length=155, verbose_name='Sujet'),
        ),
    ]
