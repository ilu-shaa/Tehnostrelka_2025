from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import json

app = FastAPI()
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
es = Elasticsearch('http://elasticsearch:9200')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/search")
async def search(query: str, size: int = 10):
    try:
        # Векторизация запроса
        query_vector = model.encode(query).tolist()
        
        # Поиск в Elasticsearch
        body = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            },
            "size": size
        }
        
        result = es.search(index='movies', body=body)
        return [{
            "title": hit["_source"]["title"],
            "year": hit["_source"]["year"],
            "poster": hit["_source"]["poster"],
            "plot": hit["_source"]["plot"],
            "author": hit["_source"]["author"],
            "reviews": hit["_source"]["reviews"]
        } for hit in result['hits']['hits']]
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/movie/{title}")
async def get_movie(title: str):
    try:
        result = es.search(index='movies', body={
            "query": {"match": {"title": title}}
        })
        return result['hits']['hits'][0]['_source']
    except:
        return {"error": "Movie not found"}