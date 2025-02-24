"""
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def get_embedding(text):
    return model.encode([text], convert_to_numpy=True)[0] if text else np.zeros(384)"""