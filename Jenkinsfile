pipeline {
    agent any

    environment {
        DAG_REMOTE = "dags"
    }

    stages {
        // ---------------------------
        // CHECKOUT
        // ---------------------------
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ---------------------------
        // FIX GIT BRANCH
        // ---------------------------
        stage('Fix Git Branch') {
            steps {
                bat '''
                echo ==== Switching to main branch ====
                git checkout main
                '''
            }
        }

        // ---------------------------
        // CREATE .env FROM JENKINS CREDENTIAL
        // ---------------------------
        stage('Create .env') {
            steps {
                withCredentials([string(credentialsId: 'env-file-content', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: ENV_CONTENT
                    echo ".env file created from Jenkins credentials."
                }
            }
        }

        // ---------------------------
        // SETUP PYTHON & INSTALL DVC
        // ---------------------------
        stage('Setup Python & DVC') {
            steps {
                bat '''
                echo ==== Creating Python virtual environment ====
                python -m venv venv
                call venv\\Scripts\\activate

                echo ==== Installing dependencies ====
                pip install --upgrade pip
                pip install dvc dagshub datasets python-dotenv
                '''
            }
        }

        // ---------------------------
        // CONFIGURE DVC REMOTE
        // ---------------------------
        stage('Configure DVC Remote') {
            steps {
                withCredentials([string(credentialsId: 'dagshub-token', variable: 'DAG_TOKEN')]) {
                    bat '''
                    echo ==== Configure DVC Remote ====
                    call venv\\Scripts\\activate

                    dvc remote modify dags --local auth basic
                    dvc remote modify dags --local user pnarkz
                    dvc remote modify dags --local password %DAG_TOKEN%
                    '''
                }
            }
        }

        // ---------------------------
        // DOWNLOAD DATASET (Python script inside Jenkins workspace)
        // ---------------------------
        stage('Download Dataset from HuggingFace') {
            steps {
                bat '''
                echo ==== Running download_data.py ====
                call venv\\Scripts\\activate
                python download_data.py
                '''
            }
        }

        // ---------------------------
        // DVC ADD
        // ---------------------------
        stage('DVC Track Data') {
            steps {
                bat '''
                echo ==== Running dvc add ====
                call venv\\Scripts\\activate
                dvc add data

                git config user.name "pnarkz"
                git config user.email "pinarkocagoz0336@gmail.com"

                git add data.dvc .gitignore
                git commit -m "ci: track data" || echo "No changes"
                '''
            }
        }

        // ---------------------------
        // PUSH DATA TO DAGSHUB
        // ---------------------------
        stage('DVC Push') {
            steps {
                bat '''
                echo ==== dvc push ====
                call venv\\Scripts\\activate
                dvc push -r dags -v
                '''
            }
        }

        // ---------------------------
        // PUSH CODE TO GITHUB
        // ---------------------------
        stage('Push Code') {
            steps {
                bat '''
                echo ==== Switching to main ====
                git checkout main

                echo ==== Pull --rebase to prevent conflicts ====
                git pull --rebase origin main

                echo ==== Stage changes ====
                git add .

                echo ==== Commit ====
                git commit -m "ci: auto update" || echo "No changes"

                echo ==== Pushing to GitHub ====
                git push origin main
                '''
            }
        }
    }

    post {
        success {
            echo '✔ Pipeline SUCCESS'
        }
        failure {
            echo '❌ Pipeline FAILED – check logs'
        }
    }
}
