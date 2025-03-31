import logging
import time
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_experimental.text_splitter import SemanticChunker

from config.embeddings import get_embeddings
from config.logger import log

def initialize_vector_store(loader: PDFPlumberLoader, use_cache=True):
    logging.info("Loading documents")
    pages = list(loader.lazy_load())  # Carrega as páginas como objetos Document

    log.debug("Initialize file store and embeddings")
    embeddings = get_embeddings(model="models/text-embedding-004")

    start_time = time.time()  # Início da medição de tempo

    if use_cache:
        fs = LocalFileStore("./cache/")
        cached_embedder = CacheBackedEmbeddings.from_bytes_store(
            embeddings, fs, namespace="sentence-transformer"
        )
    else:
        cached_embedder = embeddings

    # Create and process documents with metadata
    text_splitter = SemanticChunker(cached_embedder)
    chunks = []
    for page in pages:
        page_chunks = text_splitter.create_documents([page.page_content], metadatas=[page.metadata])
        chunks.extend(page_chunks)

    # Create and save vector store
    store = FAISS.from_documents(chunks, cached_embedder)
    store.save_local('./vectorstore')

    end_time = time.time()  # Fim da medição de tempo
    elapsed_time = end_time - start_time

    log.debug(f"Tempo de execução (cache={'ativado' if use_cache else 'desativado'}): {elapsed_time:.2f} segundos")

    # Load and return the store
    return FAISS.load_local("./vectorstore", cached_embedder, allow_dangerous_deserialization=True)