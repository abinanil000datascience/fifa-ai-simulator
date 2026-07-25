pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                script {
                    echo "Building FastAPI Backend..."
                    sh 'docker build -f Dockerfile.backend -t fifa-ai-backend:latest .'
                }
            }
        }

        stage('Run Automated Tests (CI)') {
            steps {
                script {
                    echo "Running PyTest against the Backend..."
                    sh 'docker run --rm fifa-ai-backend:latest pytest tests/test_api.py'
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                script {
                    echo "Building Streamlit Frontend..."
                    sh 'docker build -f Dockerfile.frontend -t fifa-ai-frontend:latest .'
                }
            }
        }

        stage('Deploy to Local Server (CD)') {
            steps {
                script {
                    echo "Deploying the tested containers..."
                    // This command safely restarts only the backend and frontend with the fresh code
                    // It intentionally leaves the PostgreSQL database running so no data is lost
                    sh 'docker compose up -d --no-deps backend frontend'
                }
            }
        }
    }
}