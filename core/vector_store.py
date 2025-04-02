import logging
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from core.chunk import do_chunk
from core.embedding import initialize_embedding


def initialize_vector_store(loader: PDFPlumberLoader):
    logging.info("Loading documents")
    pages = list(loader.lazy_load())
    embeddings = initialize_embedding(use_cache=False)
    chunks = do_chunk(embeddings, pages)
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local('./vectorstore')
    return FAISS.load_local("./vectorstore", embeddings, allow_dangerous_deserialization=True)


