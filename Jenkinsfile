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
                    echo "Installing Docker Compose and Deploying..."
                    sh '''
                    # 1. Download the Docker Compose plugin directly into the Jenkins container
                    mkdir -p ~/.docker/cli-plugins/
                    curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
                    chmod +x ~/.docker/cli-plugins/docker-compose
                    
                    # 2. Deploy the containers to your local machine using the correct project network
                    docker compose -p fifa-ai-simulator up -d --no-deps backend frontend
                    '''
                }
            }
        }
    }
}