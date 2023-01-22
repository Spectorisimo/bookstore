from typing import Protocol, OrderedDict
from django.db.models import QuerySet, Avg

from .models import Books, UserBooksRelation


class BooksRepositoryInterface(Protocol):
    @staticmethod
    def get_books() -> QuerySet[Books]:
        ...


class UserBooksRelationRepositoryInterface(Protocol):
    @staticmethod
    def get_relations() -> QuerySet[UserBooksRelation]:
        ...

    @staticmethod
    def get_or_create_relation(data: OrderedDict) -> QuerySet[UserBooksRelation]:
        ...


class BooksRepositoryV1:
    @staticmethod
    def get_books() -> QuerySet[Books]:
        return Books.objects.select_related('owner').prefetch_related('readers')


class UserBooksRelationRepositoryV1:
    @staticmethod
    def get_relations() -> QuerySet[UserBooksRelation]:
        return UserBooksRelation.objects.all()

    @staticmethod
    def get_or_create_relation(data: OrderedDict) -> QuerySet[UserBooksRelation]:
        return UserBooksRelation.objects.get_or_create(**data)
