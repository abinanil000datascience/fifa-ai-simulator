pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // This pulls the latest code from your GitHub repo
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

        stage('Build Frontend Image') {
            steps {
                script {
                    echo "Building Streamlit Frontend..."
                    sh 'docker build -f Dockerfile.frontend -t fifa-ai-frontend:latest .'
                }
            }
        }
    }
}