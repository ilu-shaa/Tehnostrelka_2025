from django.urls import path
from .views import search_movies, get_movie_by_title

urlpatterns = [
    path('search/', search_movies, name='search_movies'),
    path('movie/<str:title>/', get_movie_by_title, name='get_movie_by_title'),
]