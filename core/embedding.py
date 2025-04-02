import time
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

from config.embeddings import get_embeddings
from config.logger import log


def initialize_embedding(use_cache=True):
    log.debug("Initialize file store and embeddings")
    embeddings = get_embeddings(model="models/text-embedding-004")

    start_time = time.time()
    if use_cache:
        fs = LocalFileStore("./cache/")
        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            embeddings, fs, namespace="sentence-transformer"
        )
    else:
        cached_embedder = embeddings
    end_time = time.time()
    elapsed_time = end_time - start_time
    log.debug(
        f"Tempo de execução (cache={'ativado' if use_cache else 'desativado'}): {elapsed_time:.2f} segundos"
    )
    return cached_embedder
