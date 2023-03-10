# Generated by Django 4.1.5 on 2023-01-21 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_books_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBooksRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('is_booksmarks', models.BooleanField(default=False)),
                ('rating', models.PositiveSmallIntegerField(choices=[('1', 'Awful'), ('2', 'Bad'), ('3', 'Ok'), ('4', 'Good'), ('5', 'Perfect')])),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.books')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
