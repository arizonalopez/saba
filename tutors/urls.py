from django.urls import path, re_path
from . import views
from .views import LogoutView, HelloView, SuperVillianView, Logout, permission_denied_view, PublicJSON


urlpatterns = [
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('home/<int:user_id>/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('home/', HelloView.as_view()),
    path('homecome/<name>/', views.SuperVillianView.as_view()),
    path('homecome/', views.SuperVillianView.as_view()),
    path('impdates/create/', views.ImpDateCreate.as_view(), name='impdate_create'),
    path('impdates/<int:pk>/', views.ImpDateDetail.as_view(), name='impdate_detail'),
    path('impdates/<int:pk>/update/', views.ImpDateUpdate.as_view(), name='impdate_update'),
    path('impdates/<int:pk>/delete/', views.ImpDateDelete.as_view(), name='impdate_delete'),
    path('403/', permission_denied_view),
    path('json/', PublicJSON.as_view())
]

