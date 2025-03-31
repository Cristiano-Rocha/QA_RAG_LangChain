from operator import itemgetter
from typing import Annotated, List, TypedDict

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda

from llm.gemini import llm
from prompts.prompts_templates import qa_template
from core.document_processor import (
    to_lower_case,
    remove_extra_spaces_and_newlines
)

class AnswerWithSources(TypedDict):
    """An answer to the question, with sources."""
    question: str
    answer: str
    sources: Annotated[
        List[str],
        ...,
        "List of sources used to answer the question",
    ]

def extract_sources(documents: List[Document]) -> List[str]:
    """Extrai as fontes dos documentos."""
    return [doc.metadata.get("source", "unknown") for doc in documents]

extract_sources_runnable = RunnableLambda(extract_sources)

def create_rag_chain(store):
    qa_prompt = ChatPromptTemplate.from_template(qa_template)
    
    pre_processing_runnable = RunnableParallel(
        stepOne=to_lower_case,
        stepThree=remove_extra_spaces_and_newlines
    )

    return (
        {
            'context': itemgetter('question') | store.as_retriever() | pre_processing_runnable,
            'question': itemgetter('question'),
            'language': itemgetter('language'),
            'sources': itemgetter('question') | store.as_retriever() | extract_sources_runnable

        }
        | qa_prompt
        | llm.with_structured_output(AnswerWithSources)
    )