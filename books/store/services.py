from typing import Protocol, OrderedDict
from django.db.models import QuerySet
from .models import Books, UserBooksRelation
from .repository import BooksRepositoryInterface, BooksRepositoryV1, \
    UserBooksRelationRepositoryInterface, UserBooksRelationRepositoryV1


class BooksServicesInterface(Protocol):
    books_repository_interface: BooksRepositoryInterface

    def get_books(self) -> QuerySet[Books]:
        ...


class UserBooksRelationServicesInterface(Protocol):
    user_books_relation_repository_interface: UserBooksRelationRepositoryInterface

    def get_relations(self) -> QuerySet[UserBooksRelation]:
        ...

    def get_or_create_relation(self, data: OrderedDict) -> QuerySet[UserBooksRelation]:
        ...


class BooksServicesV1:
    books_repository: BooksRepositoryV1 = BooksRepositoryV1()

    def get_books(self) -> QuerySet[Books]:
        return self.books_repository.get_books()


class UserBooksRelationServicesV1:
    user_books_relation_repository: UserBooksRelationRepositoryInterface = UserBooksRelationRepositoryV1()

    def get_relations(self) -> QuerySet[UserBooksRelation]:
        return self.user_books_relation_repository.get_relations()

    def get_or_create_relation(self, data: OrderedDict) -> QuerySet[UserBooksRelation]:
        return self.user_books_relation_repository.get_or_create_relation(data)
