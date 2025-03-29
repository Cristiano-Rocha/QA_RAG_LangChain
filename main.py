from langchain import hub
from langchain.embeddings import CacheBackedEmbeddings
from langchain.prompts import Prompt
from langchain.storage import LocalFileStore
from langchain_community.document_loaders.generic import GenericLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, Runnable
from langchain_community.vectorstores import FAISS
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import FileSystemBlobLoader

from config.embeddings import get_embeddings
from config.logger import log
from llm.gemini import llm


loader = GenericLoader(
    blob_loader=FileSystemBlobLoader(
        path="storage/documents/",
        glob="*.pdf",
    ),
    blob_parser=PyPDFParser(),
)

pages = [page.page_content for page in loader.lazy_load()]

fs = LocalFileStore("./cache/")

embeddings = get_embeddings(model="models/text-embedding-004")

cached_embedder = CacheBackedEmbeddings.from_bytes_store(
 embeddings, fs, namespace="sentence-transformer"
)

text_splitter = SemanticChunker(cached_embedder)
chunks = text_splitter.create_documents(pages)
store = FAISS.from_documents(chunks, cached_embedder)
store.save_local('./vectorstore')

store = FAISS.load_local("./vectorstore", cached_embedder, allow_dangerous_deserialization=True)

qa_template = """
Você é uma assistente para tarefas de perguntas e respostas.
 Use os seguintes trechos de contexto para responder à pergunta. 
 Se você não souber a resposta, apenas diga que não sabe.
Use no máximo três frases e mantenha a resposta concisa. 
 Pergunta: {question} 
 Contexto: {context} 
 Resposta:
"""
qa_prompt = ChatPromptTemplate.from_template(qa_template)

def format_docs(docs):
    log.info("Formatando documento...")
    return "\n\n ------------".join(doc.page_content for doc in docs)

class PreprocessQuestion(Runnable):
    def to_upper_case(answer):
        return answer

    def run(self, question: str) -> str:
        return self.to_upper_case(question)




rag_chain = (
            RunnableParallel(context = store.as_retriever() | format_docs, question= RunnablePassthrough() ) |
            qa_prompt |
            llm
)

result = rag_chain.invoke("Com base no meu currículo, elabore um texto para eu falar sobre minha experiência profissional para uma entreivsta de emprego, responda em inglês.")
log.info(result.content)