from zenml.steps import step
import mlflow
import time
from tracking.mlflow_init import init_mlflow

# Örnek olarak sentence-transformers kullanımı:
from sentence_transformers import SentenceTransformer


@step
def embed_documents_step(chunks: list[dict], model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> list[dict]:
    """
    Üçüncü adım: Chunk'lar için embedding vektörleri oluşturur.
    """
    init_mlflow("rag_feature_pipeline")

    model = SentenceTransformer(model_name)
    start = time.time()
    texts = [c["chunk"] for c in chunks]
    embeddings = model.encode(texts)
    elapsed = time.time() - start

    vectors = [{"text": t, "embedding": e.tolist()} for t, e in zip(texts, embeddings)]

    with mlflow.start_run(run_name="embed_documents", nested=True):
        mlflow.log_param("model_name", model_name)
        mlflow.log_metric("vector_count", len(vectors))
        mlflow.log_metric("embed_time_sec", elapsed)
        print(f"[EMBED] {len(vectors)} vektör oluşturuldu. Süre: {elapsed:.2f} sn")
    return vectors
