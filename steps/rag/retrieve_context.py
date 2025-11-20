# steps/rag/retrieve_context.py
from zenml import step
from sentence_transformers import SentenceTransformer
from llm_engineering.infrastructure.db.qdrant import QdrantDatabaseConnector

@step
def retrieve_context(query: str = "Aziz Sancar kimdir?"):
    """
    Retrieves the most relevant context documents from Qdrant DB.
    """
    qdrant = QdrantDatabaseConnector()
    encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    q_vec = encoder.encode(query)
    results = qdrant.search(collection_name="embedded_articles", query_vector=q_vec, limit=3)

    print("\n🔍 Retrieved Context Documents:")
    contexts = []
    for r in results:
        payload = r.payload if hasattr(r, "payload") else {}
        title = payload.get("title", "Untitled")
        content = payload.get("text", "")
        print(f" - {title}")
        contexts.append(f"{title}\n{content}")

    return "\n\n".join(contexts)
