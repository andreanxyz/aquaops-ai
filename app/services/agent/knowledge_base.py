import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from app.core.config import settings

def get_chroma_client():
    return chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

def get_collection():
    client = get_chroma_client()
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(
        name="aquaops_knowledge",
        embedding_function=ef,
    )

def load_documents():
    collection = get_collection()
    docs_dir = Path("knowledge_base/documents")
    documents, metadatas, ids = [], [], []
    for i, doc_path in enumerate(docs_dir.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8")
        sections = text.split("\n## ")
        for j, section in enumerate(sections):
            if section.strip():
                documents.append(section[:2000])
                metadatas.append({"source": doc_path.name, "section": j})
                ids.append(f"{doc_path.stem}_{j}")
    if documents:
        collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Loaded {len(documents)} chunks into ChromaDB")

def query_knowledge(question: str, n_results: int = 3) -> str:
    collection = get_collection()
    results = collection.query(query_texts=[question], n_results=n_results)
    if not results["documents"] or not results["documents"][0]:
        return ""
    return "\n\n---\n\n".join(results["documents"][0])
