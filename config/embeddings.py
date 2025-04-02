from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.logger import log


def get_embeddings(model: str) -> GoogleGenerativeAIEmbeddings:
    """Retorna uma instância do GoogleGenerativeAIEmbeddings"""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model=model)
        log.info("Embeddings carregado com sucesso")
        return embeddings
    except Exception:
        log.error("Erro ao carregar o modelo de embeddings")
        raise Exception
