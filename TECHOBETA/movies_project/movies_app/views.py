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