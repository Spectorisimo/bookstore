import json

from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Books
from ..serializer import BooksSerializer
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Books, UserBooksRelation


class BooksApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
        self.book_1 = Books.objects.create(name='Testbook 1', price=200.00, author_name='Author 1', owner=self.user)
        self.book_2 = Books.objects.create(name='Testbook 2', price=200.00, author_name='BAuthor 2', owner=self.user)
        self.book_3 = Books.objects.create(name='Testbook 3 Author 1', price=20.00, author_name='Author 3')

    def test_get(self):
        url = reverse('books-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_field_by_price(self):
        url = reverse('books-list')
        response = self.client.get(url, data={'price': 200.00})
        serializer_data = BooksSerializer([self.book_1, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search_by_author_name(self):  # no difference if name contains in title or in author_name
        url = reverse('books-list')
        response = self.client.get(url, data={'search': "Author 1"})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering_by_price(self):
        url = reverse('books-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer_data = BooksSerializer([self.book_3, self.book_1, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering_by_author_name(self):
        url = reverse('books-list')
        response = self.client.get(url, data={'ordering': 'author_name'})
        serializer_data = BooksSerializer([self.book_1, self.book_3, self.book_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create_book(self):
        url = reverse('books-list')
        books_len_before = len(Books.objects.all())
        data = {
            'name': 'Clean Architechture',
            'price': 9000.00,
            'author_name': 'Robert Martin',
            'readers':[
            {
             'first_name':'Testname',
             'username':'Testusername'
            }
        ],
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        books_len_after = len(Books.objects.all())
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(books_len_after, books_len_before + 1)
        self.assertEqual(self.user, Books.objects.last().owner)

    def test_update_book_partially(self):
        url = reverse('books-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 1337.00,
            'author_name': self.book_1.author_name
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1337.00, self.book_1.price)

    def test_delete_book(self):
        url = reverse('books-detail', args=(self.book_2.id,))
        data = {
            'name': self.book_2.name,
            'price': self.book_2.price,
            'author_name': self.book_2.author_name
        }
        self.client.force_login(self.user)
        json_data = json.dumps(data)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        try:
            deleted_book = Books.objects.get(id=self.book_2.id)
        except Books.DoesNotExist:
            deleted_book = None

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(deleted_book, None)

    def test_update_book_partially_not_owner(self):
        self.user2 = User.objects.create(username='test_user2')
        url = reverse('books-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 1337.00,
            'author_name': self.book_1.author_name
        }
        self.client.force_login(self.user2)
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(200.00, self.book_1.price)

    def test_delete_not_owner(self):
        self.user2 = User.objects.create(username='test_user2')
        url = reverse('books-detail', args=(self.book_2.id,))
        data = {
            'name': self.book_2.name,
            'price': self.book_2.price,
            'author_name': self.book_2.author_name
        }
        self.client.force_login(self.user2)
        json_data = json.dumps(data)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        try:
            deleted_book = Books.objects.get(id=self.book_2.id)
        except Books.DoesNotExist:
            deleted_book = None
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(deleted_book, self.book_2)

    def test_update_book_partially_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_user2', is_staff=True)
        url = reverse('books-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 1337.00,
            'author_name': self.book_1.author_name
        }
        self.client.force_login(self.user2)
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1337.00, self.book_1.price)

    def test_delete_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_user2', is_staff=True)
        url = reverse('books-detail', args=(self.book_2.id,))
        data = {
            'name': self.book_2.name,
            'price': self.book_2.price,
            'author_name': self.book_2.author_name
        }
        self.client.force_login(self.user2)
        json_data = json.dumps(data)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        try:
            deleted_book = Books.objects.get(id=self.book_2.id)
        except Books.DoesNotExist:
            deleted_book = None

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(deleted_book, None)


class UserBooksRelationTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
        self.book_1 = Books.objects.create(name='Testbook 1', price=200.00, author_name='Author 1', owner=self.user)

    def test_patch_to_bool_fields(self):
        url = reverse('userbooksrelation-detail', args=(self.book_1.id,))
        data = {
            'like': True,  # Изменяем поле

        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')  # применяем изменение
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()  # обновляем базу
        relation = UserBooksRelation.objects.get(user=self.user, book=self.book_1)  # берем отношение, где изменили поле
        self.assertTrue(relation.like)  # проверяем
        data = {
            'is_booksmarks': True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        relation = UserBooksRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.is_booksmarks)

    def test_rating(self):
        url = reverse('userbooksrelation-detail', args=(self.book_1.id,))
        data = {
            'rating': '5',
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        relation = UserBooksRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual('5', relation.rating)

    def test_incorrect_rating(self):
        url = reverse('userbooksrelation-detail', args=(self.book_1.id,))
        data = {
            'rating': '6',
        }

        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
        self.book_1.refresh_from_db()
        relation = UserBooksRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(relation.rating, relation.rating)
