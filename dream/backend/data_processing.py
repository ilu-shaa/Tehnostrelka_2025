import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from typing import List, Dict
import config

def create_index(es: Elasticsearch, index_name: str):
    """
    Создаёт (или пересоздаёт) индекс с поддержкой k-NN.
    """
    settings = {
        "settings": {
            "index": {
                "knn": True,
                "knn.algo_param": {
                    "ef_search": 100
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {"type": "keyword"},
                "year": {"type": "integer"},
                "author": {"type": "keyword"},
                "poster": {"type": "keyword"},
                "plot": {"type": "text"},
                "user_tags": {"type": "keyword"},
                "reviews": {"type": "text"},
                "vector": {
                    "type": "knn_vector",
                    "dimension": 384  # зависит от используемой модели
                }
            }
        }
    }

    try:
        es.indices.delete(index=index_name)
    except NotFoundError:
        pass

    es.indices.create(index=index_name, body=settings)
    print(f"Индекс {index_name} создан.")

def load_csv_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df

def preprocess_data(df: pd.DataFrame) -> List[Dict]:
    movies = []
    for _, row in df.iterrows():
        user_tags = []
        if isinstance(row["user_tags"], str):
            user_tags = [tag.strip() for tag in row["user_tags"].split(",")]

        reviews_str = str(row["reviews"])  # "[{'source': 'IMDB', 'value': '8.1/10'}, ...]"

        movie = {
            "title": row["title"],
            "year": int(row["year"]),
            "author": row.get("author", ""),
            "poster": row.get("poster", ""),
            "plot": row.get("plot", ""),
            "user_tags": user_tags,
            "reviews": reviews_str
        }
        movies.append(movie)
    return movies

def embed_and_index_movies(es: Elasticsearch, movies: List[Dict]):
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    for movie in movies:
        text_for_embedding = movie["plot"] + " " + " ".join(movie["user_tags"])
        vector = model.encode(text_for_embedding).tolist()

        doc = {
            "title": movie["title"],
            "year": movie["year"],
            "author": movie["author"],
            "poster": movie["poster"],
            "plot": movie["plot"],
            "user_tags": movie["user_tags"],
            "reviews": movie["reviews"],
            "vector": vector
        }
        es.index(index=config.MOVIES_INDEX, document=doc)

    print(f"{len(movies)} фильмов проиндексировано!")

if __name__ == "__main__":
    es_client = Elasticsearch(config.ELASTICSEARCH_URL)

    # 1) Создаём/пересоздаём индекс
    create_index(es_client, config.MOVIES_INDEX)

    # 2) Загружаем CSV
    csv_path = os.path.join("data", "movies.csv")
    df = load_csv_data(csv_path)

    # 3) Предобрабатываем
    movies = preprocess_data(df)

    # 4) Векторизуем и индексируем
    embed_and_index_movies(es_client, movies)