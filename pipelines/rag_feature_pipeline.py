from zenml import pipeline
import mlflow
from tracking.mlflow_init import init_mlflow

# Step'leri import ediyoruz
from steps.rag.clean_documents_step import clean_documents_step
from steps.rag.chunk_documents_step import chunk_documents_step
from steps.rag.embed_documents_step import embed_documents_step
from steps.rag.load_to_vector_db_step import load_to_vector_db_step


@pipeline(name="rag_feature_pipeline")
def rag_feature_pipeline():
    """
    RAG Feature Pipeline
    Belgeleri temizler, parçalar, embed eder ve vektör veritabanına yükler.
    """
    # 1️⃣ Temizleme
    cleaned = clean_documents_step()
    # 2️⃣ Parçalama
    chunks = chunk_documents_step(cleaned_docs=cleaned)
    # 3️⃣ Embedding
    vectors = embed_documents_step(chunks=chunks)
    # 4️⃣ Yükleme
    collection = load_to_vector_db_step(vectors=vectors)

    return collection
