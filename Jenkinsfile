pipeline {
    agent any

    environment {
        IMAGE_NAME = 'fazilahmed/fastapi-login'
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
        
        DOCKERHUB_CREDS = credentials('dockerhub-credentials')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Cloning repository from GitHub..."
                git branch: 'main', 
                    url: 'https://github.com/Fazil711/Devops_test.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Logging into Docker Hub..."
                sh 'echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin'
                
                echo "Pushing images..."
                sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
                sh 'docker push ${IMAGE_NAME}:latest'
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
}
