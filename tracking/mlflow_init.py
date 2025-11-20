# tracking/mlflow_init.py
import os
import mlflow

def init_mlflow(experiment_name: str = "rag_feature_pipeline"):
    """Initialize MLflow connection for this project."""
    uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
    mlflow.set_tracking_uri(uri)
    mlflow.set_experiment(experiment_name)
