from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from .models import Product

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim embeddings
_cached_embeddings = {}

def get_product_embeddings():
    global _cached_embeddings
    if _cached_embeddings:
        return _cached_embeddings

    embeddings = {}
    products = Product.objects.all()

    for product in products:
        text = f"{product.name} {product.sku}"
        emb = model.encode(text)
        embeddings[product.id] = emb

    _cached_embeddings = embeddings
    return embeddings

def search_products_by_semantics(query, top_n=5):
    query_vec = model.encode(query)
    product_embeddings = get_product_embeddings()

    results = []
    for pid, emb in product_embeddings.items():
        similarity = cosine_similarity([query_vec], [emb])[0][0]
        results.append((pid, similarity))

    results.sort(key=lambda x: x[1], reverse=True)
    return [pid for pid, score in results[:top_n]]
