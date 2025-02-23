from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .models import Movie
from .forms import RegistrationForm, LoginForm

def movie_list(request):
    search_query = request.GET.get('q', '')
    genres = [
        'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
        'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
        'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'
    ]
    
    movies = Movie.objects.all().order_by('title')
    
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) | 
            Q(plot__icontains=search_query) |
            Q(author__icontains=search_query)
        ).distinct()

    return render(request, 'movies_app/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'search_query': search_query
    })

def genre_movies(request, genre):
    movies = Movie.objects.filter(user_tags__icontains=genre).order_by('title')
    return render(request, 'movies_app/movie_list.html', {
        'movies': movies,
        'genres': [
            'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
            'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'
        ],
        'genre': genre,
        'search_query': ''
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies_app/movie_detail.html', {'movie': movie})

def profile(request):
    return render(request, 'movies_app/profile.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('movie_list')
        return render(request, 'movies_app/register.html', {'form': form})
    return render(request, 'movies_app/register.html', {'form': RegistrationForm()})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('movie_list')
        return render(request, 'movies_app/login.html', {'form': form})
    return render(request, 'movies_app/login.html', {'form': LoginForm()})

def user_logout(request):
    logout(request)
    return redirect('movie_list')

from django.contrib.auth.decorators import login_required
from .models import Like

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, movie=movie).exists()
    
    return render(request, 'movies_app/movie_detail.html', {
        'movie': movie,
        'is_liked': is_liked
    })

@login_required
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    like, created = Like.objects.get_or_create(user=request.user, movie=movie)
    
    if not created:
        like.delete()
    
    return redirect('movie_detail', movie_id=movie_id)

from collections import defaultdict
from django.db.models import Count

def recommendations(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Получаем лайки текущего пользователя
    user_likes = Like.objects.filter(user=request.user).values_list('movie_id', flat=True)
    
    # Находим пользователей с похожими лайками
    similar_users = Like.objects.filter(
        movie_id__in=user_likes
    ).exclude(user=request.user).values('user').annotate(
        common_likes=Count('user')
    ).order_by('-common_likes')[:5]
    
    # Собираем рекомендации
    similar_users_ids = [u['user'] for u in similar_users]
    recommended_movies = Movie.objects.filter(
        like__user_id__in=similar_users_ids
    ).exclude(
        id__in=user_likes
    ).annotate(
        likes_count=Count('like')
    ).order_by('-likes_count')[:10]
    
    # Если рекомендаций мало, добавим популярные
    if len(recommended_movies) < 5:
        popular = Movie.objects.annotate(likes=Count('like')).order_by('-likes')[:5]
        recommended_movies = list(recommended_movies) + list(popular)
    
    return render(request, 'movies_app/recommendations.html', {
        'movies': recommended_movies
    })
