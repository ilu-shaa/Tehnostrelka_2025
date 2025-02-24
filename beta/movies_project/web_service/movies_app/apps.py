# movies_app/apps.py
from django.apps import AppConfig
import os
import pickle

EMBEDDINGS = {}  # глобальный словарь { movie_id: np.array([...]) }

class MoviesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies_app'

    def ready(self):
        # Путь к файлу кэша
        cache_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'embeddings_cache.pkl')
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
                global EMBEDDINGS
                EMBEDDINGS = data
                print(f"Loaded embeddings: {len(EMBEDDINGS)} movies")
        else:
            print("No embeddings cache found. Run build_embeddings.py first!")