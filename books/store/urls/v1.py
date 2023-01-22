from rest_framework.routers import DefaultRouter
from django.urls import path
from store.views import BooksModelViewSet,github_login_page,UserBookRelationAPI
router = DefaultRouter()
router.register(r'books', BooksModelViewSet)
router.register(r'books-relation', UserBookRelationAPI)
urlpatterns =[
    path('auth/',github_login_page),
]
urlpatterns += router.urls
