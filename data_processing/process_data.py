import pandas as pd
from ast import literal_eval
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import numpy as np

def process_and_load():
    # Загрузка данных
    df = pd.read_csv("movies.csv", converters={
        "user_tags": literal_eval,
        "reviews": literal_eval
    })
    
    # Очистка и преобразование
    df['user_tags'] = df['user_tags'].apply(lambda x: x.split(', ') if isinstance(x, str) else x)
    df['combined_text'] = df['plot'] + ' ' + df['user_tags'].apply(lambda x: ' '.join(x))
    
    # Загрузка в PostgreSQL
    engine = create_engine('postgresql://user:password@postgres/moviedb')
    df.to_sql('movies', engine, if_exists='replace', index=False)
    
    # Векторизация текста
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    vectors = model.encode(df['combined_text'].values)
    
    # Подключение к Elasticsearch
    es = Elasticsearch('http://elasticsearch:9200')
    
    # Создание индекса
    if not es.indices.exists(index='movies'):
        es.indices.create(
            index='movies',
            body={
                "mappings": {
                    "properties": {
                        "vector": {
                            "type": "dense_vector",
                            "dims": 384
                        }
                    }
                }
            }
        )
    
    # Загрузка данных
    for idx, row in df.iterrows():
        doc = {
            "title": row['title'],
            "year": int(row['year']),
            "poster": row['poster'],
            "author": row['author'],
            "reviews": row['reviews'],
            "plot": row['plot'],
            "vector": vectors[idx].tolist()
        }
        es.index(index='movies', id=idx, document=doc)

if __name__ == "__main__":
    process_and_load()