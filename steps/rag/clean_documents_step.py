from zenml.steps import step
import mlflow
from tracking.mlflow_init import init_mlflow


@step
def clean_documents_step() -> list[dict]:
    """
    İlk adım: Belgeleri temizler.
    Bu örnekte pipeline içinde test verisi üretilir.
    """
    init_mlflow("rag_feature_pipeline")

    # 🔹 Geçici test verisi
    raw_docs = [
        {"id": "1", "text": "ZenML ve MLflow ile RAG pipeline testi"},
        {"id": "2", "text": "   "},
        {"id": "3", "text": ""},
        {"id": "4", "text": "Digital Twin projesi RAG modülü"},
    ]

    with mlflow.start_run(run_name="clean_documents", nested=True):
        mlflow.log_param("raw_count", len(raw_docs))
        cleaned = [doc for doc in raw_docs if doc.get("text") and len(doc["text"].strip()) > 0]
        mlflow.log_metric("cleaned_count", len(cleaned))
        print(f"[CLEAN] Temizlenen belge sayısı: {len(cleaned)} / {len(raw_docs)}")
    return cleaned
