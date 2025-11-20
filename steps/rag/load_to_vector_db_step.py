from zenml.steps import step
import mlflow
from tracking.mlflow_init import init_mlflow


@step
def load_to_vector_db_step(vectors: list[dict], collection_name: str = "llm_twin_docs") -> str:
    """
    Dördüncü adım: Embedding vektörlerini vektör veritabanına yükler (ör. MongoDB, Qdrant, Chroma).
    Şu an için sadece sayısını logluyoruz.
    """
    init_mlflow("rag_feature_pipeline")

    with mlflow.start_run(run_name="load_vector_db", nested=True):
        mlflow.log_param("collection", collection_name)
        mlflow.log_metric("loaded_count", len(vectors))
        print(f"[LOAD] {len(vectors)} vektör {collection_name} koleksiyonuna yüklendi (simülasyon).")
    return collection_name
