from django.contrib import admin
from .models import Books,UserBooksRelation


# Register your models here.
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    ...

@admin.register(UserBooksRelation)
class UserBooksRelationAdmin(admin.ModelAdmin):
    ...
