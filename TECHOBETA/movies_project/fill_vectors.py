import django
import os
import sys
import numpy as np
from sentence_transformers import SentenceTransformer

# Установка переменной окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movies_project.settings")
django.setup()

# Импорт модели Movie
from movies_app.models import Movie

def generate_embeddings():
    # Загрузка модели SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    batch_size = 32
    
    # Получение всех объектов Movie из базы данных
    movies = Movie.objects.all()
    
    # Обработка фильмов батчами
    for i in range(0, movies.count(), batch_size):
        batch = movies[i:i+batch_size]
        # Извлечение текстов сюжетов, замена None на пустую строку
        texts = [m.plot or "" for m in batch]
        # Генерация эмбеддингов для батча
        embeddings = model.encode(texts)
        
        # Сохранение эмбеддингов в объекты Movie
        for movie, emb in zip(batch, embeddings):
            movie.plot_vector = emb.tolist()  # Предполагается, что plot_vector — это JSONField
            movie.save()

if __name__ == "__main__":
    generate_embeddings()