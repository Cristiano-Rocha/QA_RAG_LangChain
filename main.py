from langchain.chains import RetrievalQA
from config.logger import log
from core.vector_store import initialize_vector_store
from loaders.pdf_loader import loader
from core.rag_chain import create_rag_chain

store = initialize_vector_store(loader, use_cache=False)

def main():
    rag_chain = create_rag_chain(store)
    test_input = {
        "question": "Quem é o autor do relatório?",
        "language": "portugues"
    }
    result = rag_chain.invoke(test_input)
    log.info(result)

if __name__ == "__main__":
    main()
