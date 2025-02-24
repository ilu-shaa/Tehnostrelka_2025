"""
import django
django.setup()
from web_service.movies_app.models import Movie
from web_service.movies_app.nlp_utils import get_embedding
import numpy as np

for movie in Movie.objects.all():
    if not movie.embedding:
        embedding = get_embedding(movie.plot)
        movie.embedding = embedding.tobytes()
        movie.save()
        print(f"Processed: {movie.title}")
        """