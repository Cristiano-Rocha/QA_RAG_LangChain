from langchain_experimental.text_splitter import SemanticChunker


def do_chunk(embeddings, pages):
    text_splitter = SemanticChunker(embeddings)
    chunks = []
    for page in pages:
        page_chunks = text_splitter.create_documents([page.page_content], metadatas=[page.metadata])
        chunks.extend(page_chunks)
    return chunks