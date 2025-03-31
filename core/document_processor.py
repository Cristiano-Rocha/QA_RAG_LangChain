import copy
from typing import List
from langchain_core.documents import Document
from config.logger import log

def format_docs(docs: List[Document]) -> str:
    log.info("Formatando documento...")
    return "\n\n ------------".join(doc.page_content for doc in docs)

def to_lower_case(docs: List[Document]) -> List[Document]:
    log.info("Convertendo documento para lowercase...")
    processed_docs = []
    for doc in docs:
        new_doc = copy.deepcopy(doc)
        new_doc.page_content = doc.page_content.lower()
        processed_docs.append(new_doc)
    return processed_docs


def remove_extra_spaces_and_newlines(docs: List[Document]) -> List[Document]:
    log.info("Removendo linhas e espaços extras do documento...")
    processed_docs = []
    for doc in docs:
        new_doc = copy.deepcopy(doc)
        new_doc.page_content = " ".join(doc.page_content.split())
        processed_docs.append(new_doc)
    return processed_docs 