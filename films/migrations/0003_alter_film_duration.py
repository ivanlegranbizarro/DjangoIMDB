# Generated by Django 5.1.4 on 2025-01-08 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_alter_film_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
