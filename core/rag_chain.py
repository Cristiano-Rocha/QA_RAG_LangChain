from operator import itemgetter
from typing import  List
from langchain.chains.openai_functions.qa_with_structure import AnswerWithSources
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda
from llm.gemini import llm
from prompts.prompts_templates import qa_template
from core.document_processor import (
    to_lower_case,
    remove_extra_spaces_and_newlines
)

def extract_sources(documents: List[Document]) -> List[str]:
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