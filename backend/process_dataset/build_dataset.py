import faiss
import pickle
import json
import numpy as np 
from typing import List
from process_dataset.embedding import embed_chunk
from search_data.retrieve import retrieve
from rank_bm25 import BM25Okapi

def build_and_save_index(chunks: List[str], index_path: str, doc_path: str):
    embeddings = [embed_chunk(chunk) for chunk in chunks]
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, index_path)

    with open(doc_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

def load_index_and_docs(index_path: str, doc_path: str):
    index = faiss.read_index(index_path)
    with open(doc_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    return index, chunks

def add_chunks_to_index(new_chunks: List[str], index_path: str, doc_path: str):
    index = faiss.read_index(index_path)
    with open(doc_path, 'r', encoding='utf-8') as f:
        doc_store = json.load(f)


    existing_set = set(doc_store)
    filtered_chunks = [chunk for chunk in new_chunks if chunk not in existing_set]

    new_embeddings = [embed_chunk(chunk) for chunk in filtered_chunks]
    index.add(np.array(new_embeddings).astype("float32"))

    doc_store.extend(filtered_chunks)
    faiss.write_index(index, index_path)
    with open(doc_path, 'w', encoding='utf-8') as f:
        json.dump(doc_store, f, ensure_ascii=False, indent=2)

def build_and_save_bm25(chunks: List[str], bm25_path: str):
    tokenized_corpus = [doc.split() for doc in chunks]
    bm25 = BM25Okapi(tokenized_corpus)

    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)

def load_bm25(bm25_path: str) -> BM25Okapi:
    with open(bm25_path, "rb") as f:
        bm25 = pickle.load(f)
    return bm25

def add_chunks_to_bm25(new_chunks: List[str], bm25_path: str, doc_path: str):

    with open(doc_path, 'r', encoding='utf-8') as f:
        doc_store = json.load(f)

    existing_set = set(doc_store)
    filtered_chunks = [chunk for chunk in new_chunks if chunk not in existing_set]

    # extend corpus
    doc_store.extend(filtered_chunks)

    # rebuild BM25
    tokenized_corpus = [doc.split() for doc in doc_store]
    bm25 = BM25Okapi(tokenized_corpus)

    with open(bm25_path, "wb") as f:
        pickle.dump(bm25, f)

    # with open(doc_path, 'w', encoding='utf-8') as f:
    #     json.dump(doc_store, f, ensure_ascii=False, indent=2)

