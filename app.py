import streamlit as st
import os
from pathlib import Path
from config.logger import log
from core.vector_store import initialize_vector_store
from core.rag_chain import create_rag_chain
from loaders.pdf_loader import loader
from langchain_core.documents import Document

# Page configuration
st.set_page_config(page_title="Document Q&A System", page_icon="📚", layout="wide")

# Initialize session state
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "store" not in st.session_state:
    st.session_state.store = None
if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "last_sources" not in st.session_state:
    st.session_state.last_sources = None


def get_document_name(doc: Document) -> str:
    """Extract document name from metadata or source."""
    if hasattr(doc, "metadata") and "source" in doc.metadata:
        return Path(doc.metadata["source"]).name
    return "Documento desconhecido"


def get_document_path(doc: Document) -> str:
    """Extract document path from metadata."""
    if hasattr(doc, "metadata") and "source" in doc.metadata:
        return doc.metadata["source"]
    return "Caminho desconhecido"


def initialize_system():
    """Initialize the RAG system with documents."""
    with st.spinner("Initializing the system..."):
        try:
            store = initialize_vector_store(loader)
            rag_chain = create_rag_chain(store)
            st.session_state.store = store
            st.session_state.rag_chain = rag_chain
            return True
        except Exception as e:
            st.error(f"Error initializing the system: {str(e)}")
            return False


def process_question(question: str, language: str = "português"):
    """Process a question and return the answer and sources."""
    if not st.session_state.rag_chain:
        if not initialize_system():
            return None, None

    try:
        # Process the question
        result = st.session_state.rag_chain.invoke(
            {"question": question, "language": language}
        )

        # Extract sources from the result
        sources = result.get("sources")

        return result["answer"], sources
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")
        return None, None


# Main UI
st.title("📚 Document Q&A System")

# Sidebar
with st.sidebar:
    st.header("Documentos Disponíveis")
    documents_path = Path("storage/documents")
    if documents_path.exists():
        pdf_files = list(documents_path.glob("*.pdf"))
        if pdf_files:
            st.write(f"Encontrados {len(pdf_files)} documentos:")
            for pdf in pdf_files:
                st.write(f"- {pdf.name}")
        else:
            st.warning("Nenhum documento PDF encontrado na pasta storage/documents")
    else:
        st.error("Pasta storage/documents não encontrada")

# Main content
st.write("""
Este sistema permite que você faça perguntas sobre seus documentos PDF.
Os documentos são processados automaticamente e você pode fazer perguntas em diferentes idiomas.
""")

# Question input
question = st.text_area("Digite sua pergunta:", height=100)

# Language selection
language = st.selectbox(
    "Selecione o idioma da resposta:",
    ["português", "inglês", "espanhol", "francês", "italiano", "alemão"],
)

# Submit button
if st.button("Enviar Pergunta"):
    if not question:
        st.warning("Por favor, digite uma pergunta.")
    else:
        with st.spinner("Processando sua pergunta..."):
            answer, sources = process_question(question, language)
            if answer:
                st.session_state.last_question = question
                st.session_state.last_answer = answer
                st.session_state.last_sources = sources

                # Create two columns for answer and sources
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Display answer
                    st.write("### Resposta:")
                    st.write(answer)

                    # Display source summary
                    if sources:
                        st.write("### 📚 Documentos Consultados:")
                        source_files = set()
                        for doc in sources:
                            source_files.add(doc)

                        for file_name in source_files:
                            st.markdown(f"- 📄 {file_name}")

                # with col2:
                #     # Display detailed sources
                #     if sources:
                #         st.write("### 🔍 Trechos Relevantes:")
                #         for i, doc in enumerate(sources, 1):
                #             doc_name = get_document_name(doc)
                #             doc_path = get_document_path(doc)
                #             # Create a container for each source
                #             with st.container():
                #                 st.markdown(f"""
                #                     <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 5px 0;">
                #                         <div style="font-weight: bold; margin-bottom: 5px;">
                #                             <span title="{doc_path}">📄 {doc_name}</span>
                #                         </div>
                #                         <div style="font-size: 0.8em; color: #666; background-color: #f8f9fa; padding: 8px; border-radius: 3px;">
                #                             {doc.page_content[:200]}...
                #                         </div>
                #                     </div>
                #                 """, unsafe_allow_html=True)
                #
                log.info(f"Question: {question}\nAnswer: {answer}")

# Add file uploader
st.header("Upload de Novos Documentos")
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")
if uploaded_file:
    # Create documents directory if it doesn't exist
    os.makedirs("storage/documents", exist_ok=True)

    # Save the uploaded file
    file_path = os.path.join("storage/documents", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")

    # Reinitialize the system with the new document
    if initialize_system():
        st.info("Sistema atualizado com o novo documento!")

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center'>
    <p>Desenvolvido com ❤️ usando LangChain e Streamlit</p>
    <p>Versão 1.0.0</p>
</div>
""",
    unsafe_allow_html=True,
)
