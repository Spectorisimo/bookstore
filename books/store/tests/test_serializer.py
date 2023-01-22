from unittest import TestCase

from django.db.models import Avg

from ..serializer import BooksSerializer,UserBooksRelationSerializer
from ..models import Books,UserBooksRelation
from django.contrib.auth.models import User


class BookSerializerTestCase(TestCase):

    def test_books_serializer(self):
        self.user = User.objects.create(username='test_user1',first_name='Tom')
        self.user_2 = User.objects.create(username='test_user2',first_name='John')
        book_1 = Books.objects.create(name='Testbook1', price=2000.00, author_name='Author 1', owner=self.user)
        book_2 = Books.objects.create(name='Testbook2', price=200.00, author_name='Author 2', owner=self.user_2)
        UserBooksRelation.objects.create(user=self.user,book=book_1,like=True,rating=5)
        UserBooksRelation.objects.create(user=self.user_2,book=book_1,like=False,rating=4)
        books=Books.objects.all()
        data = BooksSerializer(books,many=True).data

        print(data)
        expected_data =[{
                'id': book_1.id,
                'likes_count': 1,
                'name': 'Testbook1',
                'price': '2000.00',
                'author_name': 'Author 1',
                'owner': self.user.id,
                'readers':[
                    {
                    self.user.first_name,
                    self.user.username,
                    },
                    {
                    self.user_2.first_name,
                    self.user_2.username,
                    },
                ],
            },
            {
                'id': book_2.id,
                'likes_count': 0,
                'name': 'Testbook2',
                'price': '200.00',
                'author_name': 'Author 2',
                'owner': self.user_2.id,
                'readers': [],
            }
            ]

        self.assertEqual(expected_data, data)


class UserBooksRelationTestCase(TestCase):

    def test_userbooks_relation_seriaizer(self):
        self.user = User.objects.create(username='test_user3')
        book_1 = Books.objects.create(name='Testbook1', price=2000.00, author_name='Author 1', owner=self.user)
        relation = UserBooksRelation.objects.create(book=book_1,like=True,is_booksmarks=True,rating=5)
        data = UserBooksRelationSerializer(relation).data
        expected_data ={
                'book': book_1.id,
                'like': True,
                'is_booksmarks': True,
                'rating': '5',
            }


        self.assertEqual(expected_data, data)




