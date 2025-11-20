pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Fix Branch') {
            steps {
                bat '''
                git checkout main
                '''
            }
        }

        stage('Create .env') {
            steps {
                withCredentials([string(credentialsId: 'env-file-content', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: ENV_CONTENT
                }
            }
        }

        stage('Setup Python') {
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

        // 🔥 Asıl çözüm burada: script dosyası oluşturarak çalıştırıyoruz!
        stage('Download Dataset') {
            steps {
                bat '''
                echo from datasets import load_dataset > download_data.py
                echo import os, json, shutil >> download_data.py
                echo from dotenv import load_dotenv >> download_data.py
                echo load_dotenv(".env") >> download_data.py
                echo token=os.getenv("HUGGINGFACE_ACCESS_TOKEN") >> download_data.py
                echo print("Token:", token[:10]+"...") >> download_data.py
                echo ds=load_dataset("hsena/llmtwin", token=token) >> download_data.py
                echo shutil.rmtree("data", ignore_errors=True) >> download_data.py
                echo os.makedirs("data", exist_ok=True) >> download_data.py
                echo import json >> download_data.py
                echo [open(f"data/item_{i}.json","w",encoding="utf8").write(json.dumps(row,ensure_ascii=False)) for i,row in enumerate(ds["train"])] >> download_data.py

                call venv\\Scripts\\activate
                python download_data.py
                '''
            }
        }

        stage('DVC Track') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                dvc add data
                git add data.dvc .gitignore
                git commit -m "ci: track data" || echo "No changes"
                '''
            }
        }

        stage('DVC Push') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                dvc push -r dags -v
                '''
            }
        }

        stage('Push Code') {
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
        success { echo '✔ SUCCESS' }
        failure { echo '❌ FAILED' }
    }
}
