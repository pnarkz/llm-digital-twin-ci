from zenml.steps import step
import mlflow
from tracking.mlflow_init import init_mlflow


@step
def chunk_documents_step(cleaned_docs: list[dict], chunk_size: int = 800, overlap: int = 120) -> list[dict]:
    """
    İkinci adım: Dokümanları parçalara böler (chunk).
    """
    init_mlflow("rag_feature_pipeline")

    chunks = []
    for doc in cleaned_docs:
        text = doc["text"]
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            chunks.append({"id": doc.get("id", None), "chunk": chunk})

    with mlflow.start_run(run_name="chunk_documents", nested=True):
        mlflow.log_params({"chunk_size": chunk_size, "overlap": overlap})
        mlflow.log_metric("chunk_count", len(chunks))
        print(f"[CHUNK] {len(chunks)} parça oluşturuldu.")
    return chunks
