# Generated by Django 4.1.5 on 2023-01-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_userbooksrelation_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbooksrelation',
            name='rating',
            field=models.CharField(choices=[('1', 'Awful'), ('2', 'Bad'), ('3', 'Ok'), ('4', 'Good'), ('5', 'Perfect')], max_length=1),
        ),
    ]
