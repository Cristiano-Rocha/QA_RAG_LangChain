from loguru import logger

logger.add("qa_rag_langchain.log", rotation="100 MB")
logger.add("errors.log", level="ERROR")


def configure_logging():
    return logger


log = configure_logging()
