pipeline {
    agent any

    environment {
        DAG_REMOTE = "dags"
    }

    stages {

        stage('Setup Python & DVC') {
            steps {
                powershell '''
                    python --version
                    python -m venv venv
                    .\\venv\\Scripts\\pip install --upgrade pip
                    .\\venv\\Scripts\\pip install dvc[dagshub]
                '''
            }
        }

        stage('Configure DVC Remote Auth') {
            steps {
                withCredentials([string(credentialsId: 'dagshub-token', variable: 'DAG_TOKEN')]) {
                    powershell '''
                        Write-Host "Using remote: dags"

                        .\\venv\\Scripts\\dvc remote modify dags --local auth basic
                        .\\venv\\Scripts\\dvc remote modify dags --local user pnarkz
                        .\\venv\\Scripts\\dvc remote modify dags --local password $env:DAG_TOKEN
                    '''
                }
            }
        }

        stage('DVC Add & Git Commit') {
            steps {
                powershell '''
                    git checkout main

                    if (Test-Path "data") {
                        .\\venv\\Scripts\\dvc add data
                    }

                    git config user.name "pnarkz"
                    git config user.email "pinarkocagoz0336@gmail.com"

                    git add -A
                    git commit -m "ci: auto dvc track" || echo "No changes to commit"

                    git push origin main
                '''
            }
        }

        stage('DVC Push Data') {
            steps {
                powershell '''
                    .\\venv\\Scripts\\dvc push -r dags
                '''
            }
        }
    }

    post {
        success {
            echo '✔ Pipeline SUCCESS'
        }
        failure {
            echo '❌ Pipeline FAILED — check logs'
        }
    }
}
