from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Todo, Post
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

class TodoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Todo.objects.create(title='first todo', body='a body here')

    def test_title_content(self):
        todo = Todo.objects.get(id=1)
        expected_object_name = f'{todo.title}'
        self.assertEqual(expected_object_name, 'first todo')

    def test_body_content(self):
        todo = Todo.objects.get(id=1)
        expected_object_name = f'{todo.body}'
        self.assertEqual(expected_object_name, 'a body here')

class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username='testuser1', password='abc123')
        testuser1.save()

        test_post = Post.objects.create(
            author=testuser1, title='Blog title', body='Body content....')
        
    def test_blog_content(self):
        post = Post.objects.get(id=1)
        author = f'{post.author}'
        title = f'{post.title}'
        body = f'{post.body}'
        self.assertEqual(author, 'testuser1')
        self.assertEqual(title, 'Blog title')
        self.assertEqual(body, 'Body content....')

class BookTest(APITestCase):
    @classmethod
    def setUpBook(cls):
        super(BookTest, cls).setUpBook()
        cls.superuser, created = User.objects.get_or_create(
            username='test-admin'
        )
        cls.superuser.is_active = True
        cls.superuser.is_superuser = True
        cls.superuser.save()

        cls.post = Post.objects.create(
            author=cls.superuser,
            title='Matrix',
            body='A new user'
        )
    @classmethod
    def tearDownClass(cls):
        super(BookTest).tearDownClass()
        cls.post.delete()
        cls.superuser.delete()

    def test_list_book(self):
        url = reverse('post_list')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['count'], Post.objects.count()
        )

    def test_get_book(self):
        url = reverse('post_detail', kwargs={
            'pk': self.post.pk
        })
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['body'], self.post.body
        )

    def test_create_post(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('post_list')
        data = {
            'author': self.superuser,
            'title': 'Abigere',
            'body': 'A stewpid person'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertTrue(
            Post.objects.filter(pk=response.data['id']).count() == 1
        )

    def test_create_restricted(self):
        self.client.force_authenticate(user=None)

        url = reverse('post_list')
        data = {
            'author': created.username,
            'title': 'Aljazeera',
            'body': 'A new station'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )


        
