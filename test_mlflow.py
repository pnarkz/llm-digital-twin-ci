# test_mlflow.py
import mlflow
import os

print("MLFLOW_TRACKING_URI =", os.getenv("MLFLOW_TRACKING_URI"))

# Deney ismini belirle (istersen değiştir)
mlflow.set_experiment("llm_twin_test")

with mlflow.start_run(run_name="initial_test"):
    mlflow.log_param("model_name", "test-mini")
    mlflow.log_metric("accuracy", 0.92)
    mlflow.log_metric("loss", 0.08)
    print("✅ MLflow run başarıyla loglandı!")
