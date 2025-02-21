from django.shortcuts import render, get_object_or_404
from movies_app.models import Movie

from django.shortcuts import render


def movie_list(request):
    # Все фильмы для главной страницы
    movies = Movie.objects.all()
    return render(request, 'movies_app/movie_list.html', {'movies': movies})

def genre_movies(request, genre):
    # Фильмы по жанру
    movies = Movie.objects.filter(user_tags__icontains=genre)
    return render(request, 'movies_app/movie_list.html', {'movies': movies, 'genre': genre})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies_app/movie_detail.html', {'movie': movie})


def movie_list(request):
    movies = Movie.objects.all()
    genres = ['Western', 'Romance', 'Fantasy', 'Crime', 'Biography', 'Music', 'History', 'Drama', 'Thriller', 'Adventure', 'Mystery', 'Action', 'Horror', 'Animation', 'Family', 'Sci-Fi', 'Musical', 'Comedy', 'Short', 'War', 'Sport']
    return render(request, 'movies_app/movie_list.html', {'movies': movies, 'genres': genres})

def genre_movies(request, genre):
    movies = Movie.objects.filter(user_tags__icontains=genre)
    genres = ['Western', 'Romance', 'Fantasy', 'Crime', 'Biography', 'Music', 'History', 'Drama', 'Thriller', 'Adventure', 'Mystery', 'Action', 'Horror', 'Animation', 'Family', 'Sci-Fi', 'Musical', 'Comedy', 'Short', 'War', 'Sport']
    return render(request, 'movies_app/movie_list.html', {'movies': movies, 'genres': genres, 'genre': genre})

def profile(request):
    # Логика для личного кабинета
    return render(request, 'movies_app/profile.html')




from django.shortcuts import render, redirect
from django.contrib.auth import login
from movies_app.forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистрации
            return redirect('movie_list')  # Перенаправляем на главную страницу
    else:
        form = RegistrationForm()
    return render(request, 'movies_app/register.html', {'form': form})



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('movie_list')  # Перенаправляем на главную страницу
    else:
        form = LoginForm()
    return render(request, 'movies_app/login.html', {'form': form})


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('movie_list')  # Перенаправляем на главную страницу