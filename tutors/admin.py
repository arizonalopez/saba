from django.contrib import admin
from .models import Register, Login, ImportantDate, Product, ProductPhoto, Category, Movie, UserProfile, ViralVideo
from django.http import HttpResponse
from django.db import models
from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib.auth.admin import User, Group, UserAdmin, GroupAdmin
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

# Register your models here.

class TitleFilter(admin.SimpleListFilter):
    title = 'titles'
    parameter_name = 'title'

    def lookups(self, request, model_admin):
        return [
            ('zero', 'Has no title'),
            ('one', 'Has one title'),
            ('many', 'Has more than one title')
        ]

    def queryset(self, request, queryset):
        qs = queryset.annotate(
            num_title=models.Count('title')
        )
        if self.value() == 'zero':
            qs = qs.filter(num_title=0)
        elif self.value() == 'one':
            qs = qs.filter(num_title=1)
        elif self.value() == 'many':
            qs = qs.filter(num_title__gte=2)
        return qs




class RegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'age')
    search_fields = ['age']
    ordering = ['name']

class ProductPhotoInline(admin.StackedInline):
    model = ProductPhoto
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'get_photo']
    list_editable = ['price']
    list_display_links = ['title']

    fieldset = [
        'Product', {
            'fields': ['title', 'slug', 'description', 'price']
        }
    ]
    prepolulated_fields = {'slug': ['title']}
    inline = [ProductPhotoInline]
    list_filter = [TitleFilter]

    

    def get_photo(self, obj):
        project_photos = obj.productphoto_set.all()[:1]
        if project_photos.count() > 0:
            return '''<a href='%(product_url)s' target='_blank'>
                <img src='%(photo_url)s' alt='' width='100'></a>''' % {
                    'product_url': obj.get_url_path(), 
                    'photo_url': project_photos[0].photo.url
                }
        return ''
    
    get_photo.short_description = 'Preview'
    get_photo.allow_tags = True

class UserAdminExtended(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']
    ordering = ['last_name', 'first_name', 'username']

    save_on_top = True

class GroupAdminExtended(GroupAdmin):
    list_display = ['__str__', 'display_users']
    save_on_top = True

    def display_users(self, obj):
        links = []
        for user in obj.user_set.all():
            ct = ContentType.objects.get_for_model(user)
            url = reverse(
                'admin: {}_{}_change'.format(
                    ct.app_label, ct.model
                ), args=[user.id]
            )
            links.append(
                '''<a href='{}' target='_blank'>{}</a>'''.format(
                    url, '{} {}'.format(
                        user.first_name, user.last_name
                    ).strip() or user.username
                )
            )
        return '<br>'.join(links)

    display_users.allow_tags = True
    display_users.short_description = 'Users'

class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['title']
    list_filter = ['title']




    

admin.site.register(Register, RegisterAdmin)
admin.site.register(Login)
admin.site.register(ImportantDate)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie)
admin.site.register(UserProfile)
admin.site.register(ViralVideo)
#admin.site.register(User, UserAdminExtended)
#admin.site.register(Group, GroupAdminExtended)

