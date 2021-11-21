from django.urls import path
from .views import BookListView, HelloView


urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('hello/<name>/', HelloView.as_view()),
    path('hello/', HelloView.as_view())
]