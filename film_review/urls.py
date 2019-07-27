from django.contrib import admin
from django.urls import include
from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_user, name="logout"),
    path('delete_comment/<int:pk>', views.delete_comment, name="delete_comment"),
    path('films/', views.films, name="films"),
    path('login/', views.login_user, name="login"),
    path("random_film/", views.random_film, name="random_film"),
    path("registration/", views.registration, name="registration"),
    path('accounts/<int:pk>/', views.profile, name='profile'),
    path('film/<int:pk>/', views.film, name='film'),
    path('find_random_film/', views.find_random_film, name='find_random_film'),
    path('select2/', include('django_select2.urls')),
]
