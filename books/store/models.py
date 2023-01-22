from django.db import models
from django.contrib.auth.models import User
from .constans import RatingChoises


class Books(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    author_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='my_books')
    readers = models.ManyToManyField(User, through='UserBooksRelation', related_name='read_books')

    def __str__(self):
        return f'{self.name}'


class UserBooksRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    like = models.BooleanField(default=False)
    is_booksmarks = models.BooleanField(default=False)
    rating = models.CharField(max_length=1, choices=RatingChoises.choices)

    def __str__(self):
        return f'Relation {self.user}&{self.book}|Rate:{self.rating}'
