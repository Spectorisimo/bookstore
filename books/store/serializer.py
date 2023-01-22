from rest_framework import serializers
from .models import Books, UserBooksRelation
from django.contrib.auth.models import User


class BookReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'username')


class BooksSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    readers = BookReaderSerializer(many=True,read_only=True)

    class Meta:
        model = Books
        fields = '__all__'

    def get_likes_count(self, instance):
        return UserBooksRelation.objects.filter(book=instance, like=True).count()


class UserBooksRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBooksRelation
        fields = ('book', 'like', 'is_booksmarks', 'rating')
