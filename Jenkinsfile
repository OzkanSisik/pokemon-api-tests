pipeline {
    agent any  // Use any agent instead of docker to avoid Docker-in-Docker issues
    
    environment {
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        MOCK_SERVICE_IMAGE = "ozkansisik/mock-pokemon-api:latest"
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Clean workspace first
                cleanWs()
                
                // Checkout the main API project
                git branch: 'main',
                    credentialsId: 'bc25183b-cbc9-4ac7-a68c-93808aacb47f',
                    url: 'git@github.com:OzkanSisik/pokemon-api-tests.git'
            }
        }
        
        stage('Setup Docker Environment') {
            steps {
                script {
                    // Ensure Docker is available
                    sh 'docker --version'
                    
                    // Pull the latest mock service image
                    sh "docker pull ${MOCK_SERVICE_IMAGE}"
                    
                    // Build the test image
                    sh "docker build -t pokemon-api-tests:${DOCKER_IMAGE_TAG} ."
                }
            }
        }
        
        stage('Start Mock Service') {
            steps {
                script {
                    // Start mock service container
                    sh """
                        docker run -d \
                            --name mock-service-${env.BUILD_NUMBER} \
                            --network test-network-${env.BUILD_NUMBER} \
                            -p 3001:3001 \
                            ${MOCK_SERVICE_IMAGE}
                    """
                    
                    // Create network for container communication
                    sh "docker network create test-network-${env.BUILD_NUMBER} || true"
                    
                    // Wait for mock service to be ready
                    sh """
                        timeout 60 bash -c 'until curl -f http://localhost:3001/health; do sleep 2; done' || exit 1
                    """
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Run tests in container, connecting to mock service
                    sh """
                        docker run --rm \
                            --name api-tests-${env.BUILD_NUMBER} \
                            --network test-network-${env.BUILD_NUMBER} \
                            -e BASE_URL="http://mock-service-${env.BUILD_NUMBER}:3001/api" \
                            -e PYTHONPATH="/app" \
                            pokemon-api-tests:${DOCKER_IMAGE_TAG}
                    """
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                script {
                    // Clean up containers and network
                    sh """
                        docker stop mock-service-${env.BUILD_NUMBER} || true
                        docker rm mock-service-${env.BUILD_NUMBER} || true
                        docker network rm test-network-${env.BUILD_NUMBER} || true
                        docker rmi pokemon-api-tests:${DOCKER_IMAGE_TAG} || true
                    """
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Ensure cleanup happens even if pipeline fails
                sh """
                    docker stop mock-service-${env.BUILD_NUMBER} || true
                    docker rm mock-service-${env.BUILD_NUMBER} || true
                    docker network rm test-network-${env.BUILD_NUMBER} || true
                    docker rmi pokemon-api-tests:${DOCKER_IMAGE_TAG} || true
                """
            }
        }
    }
}