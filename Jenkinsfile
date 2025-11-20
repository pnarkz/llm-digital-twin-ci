pipeline {
    agent any

    environment {
        DAG_REMOTE = "dags"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Fix Git Branch') {
            steps {
                bat '''
                echo ==== Switching from detached HEAD to main branch ====
                git checkout main
                '''
            }
        }

        stage('Create .env') {
            steps {
                withCredentials([string(credentialsId: 'env-file-content', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: ENV_CONTENT
                    echo ".env created from Jenkins credentials."
                }
            }
        }

        stage('Setup Python & DVC') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install dvc dagshub datasets python-dotenv
                '''
            }
        }

        stage('Configure DVC Remote') {
            steps {
                withCredentials([string(credentialsId: 'dagshub-token', variable: 'DAG_TOKEN')]) {
                    bat '''
                    call venv\\Scripts\\activate
                    dvc remote modify dags --local auth basic
                    dvc remote modify dags --local user pnarkz
                    dvc remote modify dags --local password %DAG_TOKEN%
                    '''
                }
            }
        }

        // 🔥 %100 ÇALIŞAN ESKİ METOT — python <<EOF
        stage('Download Dataset from HuggingFace') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python - << "EOF"
from datasets import load_dataset
import os, json, shutil
from dotenv import load_dotenv

load_dotenv(".env")
token = os.getenv("HUGGINGFACE_ACCESS_TOKEN")
print("Token loaded:", token[:10] + "...")

# temiz klasör
if os.path.exists("data"):
    shutil.rmtree("data")
os.makedirs("data", exist_ok=True)

# dataset indir
ds = load_dataset("hsena/llmtwin", token=token)

# json kaydet
for i, row in enumerate(ds["train"]):
    with open(f"data/item_{i}.json","w",encoding="utf-8") as f:
        json.dump(row, f, ensure_ascii=False)

print("Dataset downloaded successfully.")
EOF
                '''
            }
        }

        stage('DVC Track Data') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                dvc add data
                git config user.name "pnarkz"
                git config user.email "pinarkocagoz0336@gmail.com"
                git add data.dvc .gitignore
                git commit -m "ci: dvc track dataset" || echo "No changes"
                '''
            }
        }

        stage('DVC Push Data') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                dvc push -r dags -v
                '''
            }
        }

        stage('Push Code to GitHub') {
            steps {
                bat '''
                git checkout main
                git add .
                git commit -m "ci: auto update" || echo "No changes"
                git push origin main
                '''
            }
        }
    }

    post {
        success { echo '✔ Pipeline SUCCESS' }
        failure { echo '❌ Pipeline FAILED — check logs' }
    }
}
