pipeline {
    agent any

    environment {
        DAG_REMOTE = "dags"
    }

    stages {

        /* --------------------------------
           CHECKOUT REPO
        -------------------------------- */
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        /* --------------------------------
           FIX DETACHED HEAD
        -------------------------------- */
        stage('Fix Git Branch') {
            steps {
                bat """
                echo ==== Switching from detached HEAD to main ====
                git fetch --all
                git checkout main
                """
            }
        }

        /* --------------------------------
           CREATE .env FILE FROM CREDENTIAL
        -------------------------------- */
        stage('Create .env') {
            steps {
                withCredentials([string(credentialsId: 'env-file-content', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: ENV_CONTENT
                    echo ".env created."
                }
            }
        }

        /* --------------------------------
           PYTHON + DVC SETUP
        -------------------------------- */
        stage('Setup Python & DVC') {
            steps {
                bat """
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install dvc dagshub datasets python-dotenv
                """
            }
        }

        /* --------------------------------
           CONFIGURE DVC REMOTE (DAGSHUB)
        -------------------------------- */
        stage('Configure DVC Remote') {
            steps {
                withCredentials([string(credentialsId: 'dagshub-token', variable: 'DAG_TOKEN')]) {
                    bat """
                    call venv\\Scripts\\activate
                    dvc remote modify dags --local auth basic
                    dvc remote modify dags --local user pnarkz
                    dvc remote modify dags --local password %DAG_TOKEN%
                    """
                }
            }
        }

        /* --------------------------------
           DOWNLOAD DATASET FROM HF
        -------------------------------- */
        stage('Download Dataset from HuggingFace') {
            steps {
                bat """
                call venv\\Scripts\\activate
                python download_data.py
                """
            }
        }

        /* --------------------------------
           DVC ADD
        -------------------------------- */
        stage('DVC Track Data') {
            steps {
                bat """
                call venv\\Scripts\\activate
                dvc add data
                git config user.name "pnarkz"
                git config user.email "pinarkocagoz0336@gmail.com"
                git add data.dvc .gitignore
                git commit -m "ci: dvc track dataset" || echo No changes
                """
            }
        }

        /* --------------------------------
           DVC PUSH → DAGSHUB
        -------------------------------- */
        stage('DVC Push Data') {
            steps {
                bat """
                call venv\\Scripts\\activate
                dvc push -r dags -v
                """
            }
        }

        /* --------------------------------
           FIX GIT DIVERGE + AUTH PUSH TO GITHUB
        -------------------------------- */
        stage('Push Code to GitHub') {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_PASS'
                )]) {
                    bat """
                    echo ==== Resetting local branch to match GitHub ====
                    git fetch origin
                    git reset --hard origin/main

                    echo ==== Commit local CI changes ====
                    git add .
                    git commit -m "ci: auto update" || echo No changes

                    echo ==== Pushing safely with credentials ====
                    git push https://%GIT_USER%:%GIT_PASS%@github.com/pnarkz/llm-digital-twin-ci.git main --force-with-lease
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✔ Pipeline SUCCESS"
        }
        failure {
            echo "❌ Pipeline FAILED — check logs"
        }
    }
}
