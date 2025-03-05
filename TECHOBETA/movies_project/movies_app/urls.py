from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('genre/<str:genre>/', views.genre_movies, name='genre_movies'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('toggle_like/<int:movie_id>/', views.toggle_like, name='toggle_like'),
    path('combined_search/', views.combined_search, name='combined_search'),


]