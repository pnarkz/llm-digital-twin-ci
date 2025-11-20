# pipelines/rag.py
from zenml import pipeline
from steps.rag.retrieve_context import retrieve_context
from steps.rag.generate_response import generate_response

@pipeline(enable_cache=False)
def rag():
    context = retrieve_context()
    generate_response(context)
