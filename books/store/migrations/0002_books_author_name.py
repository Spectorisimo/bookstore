# Generated by Django 4.1.5 on 2023-01-19 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='author_name',
            field=models.CharField(default='Unkown Author', max_length=255),
            preserve_default=False,
        ),
    ]