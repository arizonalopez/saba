from django.contrib import admin

# Register your models here.
from .models import Book, Todo, Post

class PostAdmin(admin.ModelAdmin):
    context_1 = {'fields': ['title', 'author']}
    context_2 = {'fields': ['body']}
    fieldsets = [(None, context_1),
        ('Post Information', context_2)
    ]



admin.site.register(Book)
admin.site.register(Todo)
admin.site.register(Post, PostAdmin)
