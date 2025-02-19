from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import config

# Инициализируем (пока без пулинга)
es = Elasticsearch(config.ELASTICSEARCH_URL)
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

@api_view(['POST'])
def search_movies(request):
    """
    Поиск фильмов по вектору (plot + user_tags).
    Принимает JSON вида { "query": "...", "k": 5 }
    """
    data = request.data
    query_text = data.get('query', '')
    k = data.get('k', 5)

    query_vector = model.encode(query_text).tolist()

    knn_body = {
        "knn": {
            "field": "vector",
            "query_vector": query_vector,
            "k": k,
            "num_candidates": k + 10
        }
    }

    response = es.search(index=config.MOVIES_INDEX, knn=knn_body)
    hits = response["hits"]["hits"]

    results = []
    for hit in hits:
        source = hit["_source"]
        results.append({
            "title": source["title"],
            "year": source["year"],
            "author": source["author"],
            "poster": source["poster"],
            "plot": source["plot"],
            "score": hit["_score"],
        })
    return Response(results)

@api_view(['GET'])
def get_movie_by_title(request, title: str):
    """
    Поиск фильма по точному совпадению title
    """
    query = {
        "query": {
            "term": {
                "title.keyword": title
            }
        }
    }
    resp = es.search(index=config.MOVIES_INDEX, body=query)

    if resp["hits"]["hits"]:
        return Response(resp["hits"]["hits"][0]["_source"])
    return Response({"error": "Movie not found"}, status=404)