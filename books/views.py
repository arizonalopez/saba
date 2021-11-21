from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, View


# Create your views here.
from .models import Book


class BookListView(ListView):
    model = Book
    template = 'books/book_list.html'

class HelloView(View):
    def get(self, request, name='World'):
        return HttpResponse(f'Hello {name}!')


