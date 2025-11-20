pipeline {
    agent any

    environment {
        ENV_FILE = ".env"
    }

    stages {

        stage('Setup Python Environment') {
            steps {
                bat '''
                echo ==== Setting up Python Environment ====
                python -m venv venv
                call venv\\Scripts\\activate

                pip install --upgrade pip
                pip install dvc dagshub dvc[http] python-dotenv datasets

                echo Environment ready.
                '''
            }
        }

        stage('Load .env Variables') {
            steps {
                bat '''
                echo ==== Loading .env Environment Variables ====                
                for /f "tokens=1,2 delims==" %%a in (%ENV_FILE%) do (
                    set %%a=%%b
                )
                echo HUGGINGFACE_ACCESS_TOKEN loaded.
                '''
            }
        }

        stage('Download Dataset from HuggingFace') {
            steps {
                bat '''
                echo ==== Downloading Dataset hsena/llmtwin ====
                call venv\\Scripts\\activate

                python - << EOF
import os
from datasets import load_dataset
from dotenv import load_dotenv
import shutil

# Load .env file
load_dotenv(".env")

hf_token = os.getenv("HUGGINGFACE_ACCESS_TOKEN")
if not hf_token:
    raise ValueError("HUGGINGFACE_ACCESS_TOKEN not found in environment!")

print("Token loaded successfully:", hf_token[:10] + "...")

# HuggingFace configuration
os.environ["HF_TOKEN"] = hf_token
os.environ["HUGGINGFACE_HUB_TOKEN"] = hf_token
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = hf_token

# Download dataset
ds = load_dataset("hsena/llmtwin", token=hf_token)

# Reset data/ dir
if os.path.exists("data"):
    shutil.rmtree("data")
os.makedirs("data", exist_ok=True)

# Save dataset entries
for i, row in enumerate(ds["train"]):
    with open(f"data/item_{i}.json", "w", encoding="utf-8") as f:
        f.write(str(row))

print("Dataset downloaded to data/")
EOF
                '''
            }
        }

        stage('DVC Track Data') {
            steps {
                bat '''
                echo ==== Tracking Data with DVC ====
                call venv\\Scripts\\activate

                dvc add data
                git add data.dvc .gitignore
                git commit -m "Track dataset hsena/llmtwin via Jenkins"
                '''
            }
        }

        stage('Push DVC Data to DagsHub') {
            steps {
                bat '''
                echo ==== Pushing Data to DagsHub ====
                call venv\\Scripts\\activate
                dvc push -r dags -v
                '''
            }
        }

        stage('Push Code to GitHub') {
            steps {
                bat '''
                echo ==== Pushing Code to GitHub ====
                git add .
                git commit -m "Jenkins auto-commit"
                git push origin main
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}
