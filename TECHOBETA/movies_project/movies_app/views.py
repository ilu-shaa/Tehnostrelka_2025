from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Movie, Like
from .forms import RegistrationForm, LoginForm
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
from django.shortcuts import render
from django.db.models import Q
from .models import Movie
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def combined_search(request):
    search_query = request.GET.get('q', '').strip()

    # Обычный поиск (точные совпадения)
    movies = Movie.objects.all().order_by('title')
    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query) | 
            Q(plot__icontains=search_query) |
            Q(author__icontains=search_query)
        ).distinct()

    # Семантический поиск (если есть запрос)
    if search_query:
        query_embedding = model.encode(search_query)
        semantic_results = []

        for movie in Movie.objects.all():
            if not movie.plot_vector:
                continue
            movie_vector = np.array(movie.get_plot_vector(), dtype=np.float32)
            dot = np.dot(query_embedding, movie_vector)
            norm_a = np.linalg.norm(query_embedding)
            norm_b = np.linalg.norm(movie_vector)
            similarity = dot / (norm_a * norm_b) if norm_a != 0 and norm_b != 0 else 0.0
            semantic_results.append((movie, similarity))

        # Сортируем по убыванию сходства
        semantic_results.sort(key=lambda x: x[1], reverse=True)
        semantic_movies = [r[0] for r in semantic_results[:20]]

        # Объединяем результаты обычного и семантического поиска
        # Убираем дубликаты с помощью set
        combined_movies = list(set(movies) | set(semantic_movies))
    else:
        combined_movies = movies

    return render(request, 'movies_app/combined_search.html', {
        'movies': combined_movies,
        'search_query': search_query,
        'genres': [
            'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
            'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
            'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'
        ]
    })

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

@login_required
def profile(request):
    # 1. Получаем все понравившиеся фильмы
    user_liked_movie_ids = Like.objects.filter(user=request.user).values_list('movie_id', flat=True)
    user_liked_movies = Movie.objects.filter(id__in=user_liked_movie_ids)

    # 2. Собираем все жанры (user_tags) у понравившихся фильмов
    liked_genres = set()
    for movie in user_liked_movies:
        if movie.user_tags:
            tags = [tag.strip().lower() for tag in movie.user_tags.split(',')]
            liked_genres.update(tags)

    # 3. Если жанров нет, отдаём популярные фильмы
    if not liked_genres:
        popular_movies = Movie.objects.annotate(likes_count=Count('like')).order_by('-likes_count')[:10]
        return render(request, 'movies_app/profile.html', {
            'movies': popular_movies
        })
    
    # 4. Строим запрос на похожие жанры
    query = Q()
    for genre in liked_genres:
        query |= Q(user_tags__icontains=genre)

    # Исключаем фильмы, уже лайкнутые пользователем
    recommended_movies = (Movie.objects.filter(query)
                                      .exclude(id__in=user_liked_movie_ids)
                                      .annotate(likes_count=Count('like'))
                                      .order_by('-likes_count'))

    # 5. Если рекомендаций меньше 10, добавим популярные
    if recommended_movies.count() < 10:
        popular_movies = Movie.objects.annotate(likes_count=Count('like')).order_by('-likes_count')[:10]
        recommended_movies = list(recommended_movies) + list(popular_movies)

    return render(request, 'movies_app/profile.html', {
        'movies': recommended_movies
    })
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

from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Like, Comment
from .forms import CommentForm

# views.py (у вас уже есть эта функция, покажу лишь фрагмент с комментариями)

import json
from django.shortcuts import render, get_object_or_404
from .models import Movie, Like, Comment
from .forms import CommentForm

from django.shortcuts import render, get_object_or_404
from .models import Movie, Like, Comment
from .forms import CommentForm
import json

from django.shortcuts import render, get_object_or_404
from .models import Movie, Like, Comment
from .forms import CommentForm
import json

import json
from django.shortcuts import render, get_object_or_404
from .models import Movie, Like, Comment
from .forms import CommentForm

import ast  # Добавляем модуль ast
import json
from django.shortcuts import render, get_object_or_404
from .models import Movie, Like, Comment
from .forms import CommentForm

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, movie=movie).exists()

    # Подгружаем комментарии
    comments = movie.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie = movie
            comment.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = CommentForm()

    # Получаем рецензии из поля reviews
    reviews = []
    if movie.reviews:
        try:
            # Пытаемся обработать как JSON
            reviews = json.loads(movie.reviews)
        except json.JSONDecodeError:
            try:
                # Если JSON не удалось обработать, пробуем ast.literal_eval
                reviews = ast.literal_eval(movie.reviews)
            except (ValueError, SyntaxError) as e:
                print(f"Ошибка при обработке reviews: {e}")
                reviews = []

    # Отладочный вывод для проверки данных
    print("Рецензии:", reviews)

    return render(request, 'movies_app/movie_detail.html', {
        'movie': movie,
        'is_liked': is_liked,
        'comments': comments,
        'form': form,
        'reviews': reviews
    })
    
@login_required
def toggle_like(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    like, created = Like.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        like.delete()
    # после переключения лайка вернуться на detail или рекомендации
    return redirect('movie_detail', movie_id=movie_id)


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Movie, Like

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Movie, Like, Comment
from .forms import RegistrationForm, LoginForm, CommentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Movie, Like, Comment
from .forms import RegistrationForm, LoginForm, CommentForm

@login_required
def recommendations(request):
    # Получаем все фильмы, которые лайкнул текущий пользователь
    user_liked_movie_ids = Like.objects.filter(user=request.user).values_list('movie_id', flat=True)
    user_liked_movies = Movie.objects.filter(id__in=user_liked_movie_ids)

    # Собираем все жанры, которые встречаются в понравившихся фильмах
    liked_genres = set()
    for movie in user_liked_movies:
        if movie.user_tags:
            # Предполагаем, что жанры хранятся в виде "Action, Drama" (через запятую)
            tags = [tag.strip().lower() for tag in movie.user_tags.split(',')]
            liked_genres.update(tags)  # добавляем в set()

    # Если пользователь не лайкнул ни одного фильма, показываем популярные фильмы
    if not liked_genres:
        popular_movies = Movie.objects.annotate(likes_count=Count('like')).order_by('-likes_count')[:10]
        return render(request, 'movies_app/recommendations.html', {
            'movies': popular_movies
        })

    # Ищем фильмы, которые содержат жанры из liked_genres
    # Используем Q-объекты для поиска по нескольким жанрам
    query = Q()
    for genre in liked_genres:
        query |= Q(user_tags__icontains=genre)

    # Исключаем фильмы, которые пользователь уже лайкнул
    recommended_movies = Movie.objects.filter(query).exclude(id__in=user_liked_movie_ids)\
                                      .annotate(likes_count=Count('like'))\
                                      .order_by('-likes_count')

    # Если рекомендаций мало, добавляем популярные фильмы
    if recommended_movies.count() < 10:
        popular_movies = Movie.objects.annotate(likes_count=Count('like')).order_by('-likes_count')[:10]
        recommended_movies = list(recommended_movies) + list(popular_movies)

    return render(request, 'movies_app/recommendations.html', {
        'movies': recommended_movies
    })