# Generated by Django 4.1.5 on 2023-01-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_userbooksrelation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbooksrelation',
            name='rating',
            field=models.IntegerField(choices=[('1', 'Awful'), ('2', 'Bad'), ('3', 'Ok'), ('4', 'Good'), ('5', 'Perfect')]),
        ),
    ]
