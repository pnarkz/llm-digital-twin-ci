# pipelines/rag_inference_pipeline.py
from zenml import pipeline
from llm_engineering.domain.queries import Query

# RAG adımlarını içe aktar
from llm_engineering.application.rag.self_query import SelfQuery
from llm_engineering.application.rag.retriever import Retriever
from llm_engineering.application.rag.reranking import Reranker
from steps.rag.generate_response import generate_response


@pipeline(enable_cache=False)
def rag_inference_pipeline(question: str = "Aziz Sancar kimdir?"):
    """
    Full RAG inference pipeline:
    1. SelfQuery → sorgudan yazar çıkar
    2. Retriever → Qdrant'tan doküman getir
    3. Reranker → en alakalı dokümanları sırala
    4. Generator → yanıt üret (OpenAI)
    """
    # 1️⃣ SelfQuery
    query = Query.from_str(question)
    query = SelfQuery().generate(query)

    # 2️⃣ Retriever
    retriever = Retriever()
    chunks = retriever.retrieve(query)

    # 3️⃣ Reranker
    reranker = Reranker()
    reranked_chunks = reranker.generate(query, chunks, keep_top_k=3)

    # 4️⃣ Generator (OpenAI yanıt üretimi)
    context = "\n\n".join([chunk.content for chunk in reranked_chunks])
    generate_response(context=context, query=question)
