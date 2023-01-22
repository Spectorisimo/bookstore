from django.urls import path,include
urlpatterns=[
    path('',include('store.urls.v1')),

]