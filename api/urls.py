from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter
from .views import BookAPIView, DetailTodo, ListTodo, PostList, PostDetail, posts_list, UserList, UserDetail
from .views import UserViewSet, PostViewSet


router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', BookAPIView.as_view()),
    path('<int:pk>/', DetailTodo.as_view()),
    path('home/', ListTodo.as_view()),
    path('home/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('about/', PostList.as_view(), name='post_list'),
    path('look/<int:pk>/', posts_list),
    path('users/', UserList.as_view()),
    #path('docs/', include_docs_urls(title='POLLS API')),
    path('users/<int:pk>/', UserDetail.as_view())
]

urlpatterns += router.urls

