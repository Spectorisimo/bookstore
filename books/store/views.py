from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .services import BooksServicesV1, UserBooksRelationServicesV1
from .serializer import BooksSerializer,UserBooksRelationSerializer
from django_filters.rest_framework.backends import DjangoFilterBackend
from .permissions import CustomIsAuthenticatedOrReadOnlyOrStaff


class BooksModelViewSet(ModelViewSet):
    books_services = BooksServicesV1()
    queryset = books_services.get_books()
    serializer_class = BooksSerializer
    permission_classes = [CustomIsAuthenticatedOrReadOnlyOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationAPI(UpdateModelMixin, GenericViewSet, ):

    user_book_relation_services = UserBooksRelationServicesV1()
    queryset = user_book_relation_services.get_relations()
    serializer_class = UserBooksRelationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'book'

    def get_object(self):
        obj, _ = self.user_book_relation_services.get_or_create_relation(data={'user':self.request.user,
                                                                         'book_id':self.kwargs['book']})
        print('created',_)
        return obj
def github_login_page(request):
    return render(request, 'login.html')
