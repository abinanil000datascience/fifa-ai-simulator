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

        stage('Run Automated Tests') {
            steps {
                script {
                    echo "Running PyTest against the Backend..."
                    // We spin up a temporary container from the image we just built to run the tests
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
    }
}