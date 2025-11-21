pipeline {
    agent any

    environment {
        DAG_REMOTE = "dags"
        VENV = "venv\\Scripts"
    }

    stages {

        /* --------------------------------------------------------
         * 1. CHECKOUT
         * --------------------------------------------------------*/
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        /* --------------------------------------------------------
         * 2. Fix Branch (Detached HEAD sorununu çözer)
         * --------------------------------------------------------*/
        stage('Fix Branch') {
            steps {
                bat '''
                git checkout main
                '''
            }
        }

        /* --------------------------------------------------------
         * 3. Create .env from Jenkins Credentials
         * --------------------------------------------------------*/
        stage('Create .env') {
            steps {
                withCredentials([string(credentialsId: 'env-file-content', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: ENV_CONTENT
                }
            }
        }

        /* --------------------------------------------------------
         * 4. Python + DVC + MLflow + Security Dependencies
         * --------------------------------------------------------*/
        stage('Setup Python') {
            steps {
                bat '''
                python -m venv venv
                call %VENV%\\activate

                pip install --upgrade pip
                pip install dvc[dagshub] datasets python-dotenv mlflow pip-audit
                '''
            }
        }

        /* --------------------------------------------------------
         * 5. Security Scan (OWASP ML06 + LLM05)
         * --------------------------------------------------------*/
        stage('Security Scan') {
            steps {
                bat '''
                call %VENV%\\activate
                python security/security_scan.py
                python security/data_security_checks.py
                '''
            }
        }

        /* --------------------------------------------------------
         * 6. Configure DVC Remote (DagsHub)
         * --------------------------------------------------------*/
        stage('Configure DVC Remote') {
            steps {
                withCredentials([string(credentialsId: 'dagshub-token', variable: 'DAG_TOKEN')]) {
                    bat '''
                    call %VENV%\\activate

                    dvc remote modify dags --local auth basic
                    dvc remote modify dags --local user pnarkz
                    dvc remote modify dags --local password %DAG_TOKEN%
                    '''
                }
            }
        }

        /* --------------------------------------------------------
         * 7. Download Dataset (HuggingFace → /data)
         * --------------------------------------------------------*/
        stage('Download Dataset') {
            steps {
                bat '''
                call %VENV%\\activate
                python tools/download_data.py
                '''
            }
        }

        /* --------------------------------------------------------
         * 8. Track Data with DVC (CRITICAL fix: no untracked file error)
         * --------------------------------------------------------*/
        stage('DVC Track') {
            steps {
                bat '''
                call %VENV%\\activate

                REM Fix Git identity
                git config user.name "pnarkz"
                git config user.email "pinarkocagoz0336@gmail.com"

                dvc add data

                git add data.dvc data/.gitignore
                git commit -m "ci: track dataset" || echo "No changes"
                '''
            }
        }

        /* --------------------------------------------------------
         * 9. Push Data to DagsHub
         * --------------------------------------------------------*/
        stage('DVC Push') {
            steps {
                bat '''
                call %VENV%\\activate
                dvc push -r dags
                '''
            }
        }

        /* --------------------------------------------------------
         * 10. Push Code to GitHub (only staged changes)
         * --------------------------------------------------------*/
        stage('Push Code') {
            steps {
                bat '''
                git checkout main

                git add -A
                git commit -m "ci: auto update" || echo "No changes"

                git push origin main
                '''
            }
        }
    }

    /* --------------------------------------------------------
     * POST
     * --------------------------------------------------------*/
    post {
        success {
            echo "✔ Pipeline SUCCESS"
        }
        failure {
            echo "❌ Pipeline FAILED — check logs"
        }
    }
}
