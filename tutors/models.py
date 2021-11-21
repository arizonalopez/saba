from django.db import models
from django.urls import reverse
from .validator import validate_name
import os
from django.contrib.auth.models import User
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey, TreeManyToManyField
from django.utils.timezone import now as timezone_now


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'products/{0}/{1}{2}'.format(
        instance.product.slug, now.strftime('%Y%m%d%H%M%S'), filename_ext.lower()
    )

class RegisterManager(models.Manager):
    def random_name(self):
        return self.filter(phone='07032880291')

# Create your models here.
class Register(models.Model):
    USER_TYPES = (
        (0, 'Ordinary'),
        (1, 'SuperHero')
    )
    name = models.CharField(verbose_name='Name', max_length=100, null=True, blank=True, unique=True)
    phone = models.CharField(verbose_name='Phone Number', null=True, max_length=50, unique=True)
    age = models.PositiveIntegerField(verbose_name='Age', null=True)
    birthday = models.DateField(verbose_name='Date Of Birth', null=True)
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True, null=True)
    modified = models.DateTimeField(verbose_name='Modified', auto_now=True, null=True)
    user_type = models.IntegerField(verbose_name='User Type', null=True, choices=USER_TYPES)
    #price = models.DecimalField(verbose_name='Price ($)', max_digits=8, decimal_places=2, blank=True, null=True)
    #photo = models.ImageField(verbose_name='Photo', upload_to=upload_to, null=True)
    #email = models.EmailField(verbose_name='Email', max_length=100, null=True)
    #password = models.CharField(verbose_name='Password', max_length=100)

    custom_manager = RegisterManager()
    

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('about')

class Login(models.Model):
    #login = models.ForeignKey(Register, verbose_name='Login', on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name='Name', max_length=100, null=True)
    password = models.CharField(verbose_name='Password', max_length=100, default='*******')


    def __str__(self):
        return self.name

class ImportantDate(models.Model):
    date = models.DateField()
    desc = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('register')

class Product(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)
    slug = models.SlugField(verbose_name='Slug', max_length=200)
    description = models.TextField(verbose_name='Description', blank=True)
    price = models.DecimalField(verbose_name='Price ($)', max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_url_path(self):
        try:
            return reverse('product_detail', kwargs={'slug': self.slug})
        except NoReverseMatch:
            return reverse('about')

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name="Photo", upload_to=upload_to)

    def __str__(self):
        return self.photo.name

class Category(MPTTModel, models.Model):
    parent = TreeForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=200)

    def __str__(self):
       return self.title

    class Meta:
        ordering = ['tree_id', 'lft']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories' 

class Movie(models.Model):
    title = models.CharField('Title', max_length=255)
    categories = TreeManyToManyField(Category, verbose_name='Categories')

    def __str__(self):
       return self.title

    class Meta:
        verbose_name = 'Movies' 
        verbose_name_plural = 'Movies'

class UserProfile(models.Model):
    user_auth = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Image', default='default.png', upload_to='profile_pics')
    #phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, default=None, blank=True)
    #born_date = models.DateField(verbose_name='Born Date', null=True, default=None, blank=True)
    #last_connection = models.DateTimeField(verbose_name='Date of last connection', null=True, default=None, blank=True)
    #year_seniority = models.IntegerField(verbose_name='Seniority', default=0)

    def __str__(self):
        return self.user_auth.username

class ViralVideo(models.Model):
    title = models.CharField(
        verbose_name='Title', max_length=200, blank=True
    )
    embed_code = models.TextField(verbose_name='Youtube embed code', blank=True)
    desktop_impressions = models.PositiveIntegerField(
        verbose_name='Desktop impression', default=0
    )
    mobile_impressions = models.PositiveIntegerField(
        verbose_name='Mobile impression', default=0
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_url_path(self):
        return reverse(
            'viral_video_detail',
            kwargs={'id': str(self.id)}
        )

class CreatorMixin(models.Model):
    creator = models.ForeignKey(User, verbose_name='Creator', editable=False, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        from tutors.middleware import get_current_user
        if not self.creator:
            self.creator = get_current_user()
        super(CreatorMixin).save(*args, **kwargs)
    save.alters_data = True

    class Meta:
        abstract = True
