pipeline {
    agent any
    
    environment {
        // Define environment variables for the pipeline
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = "pokemon-api-tests-${env.BUILD_NUMBER}"
    }
    
    options {
        // Pipeline options for better reliability
        timeout(time: 10, unit: 'MINUTES')
        retry(1)
        timestamps()
        ansiColor('xterm')
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "🔍 Checking out repository..."
                    
                    // Clean workspace manually (no plugin needed)
                    sh 'rm -rf * || true'
                    
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: '*/main']],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [
                            [$class: 'CleanBeforeCheckout'],
                            [$class: 'CleanCheckout']
                        ],
                        submoduleCfg: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-ssh-key',
                    url: 'git@github.com:OzkanSisik/pokemon-api-tests.git'
                        ]]
                    ])
                    
                    echo "✅ Repository checked out successfully"
                }
            }
        }
        
        stage('Pull Latest Mock Service Image') {
            steps {
                script {
                    echo "📦 Pulling latest mock-service image from Docker Hub..."
                    sh 'docker pull ozkansisik/mock-pokemon-api:latest'
                }
            }
        }
        stage('Validate Environment') {
            steps {
                script {
                    echo " Validating Jenkins environment..."
                    
                    // Check if we can access Docker socket
                    sh 'ls -la /var/run/docker.sock || echo "Docker socket not found"'
                    
                    // Try to run Docker commands using the host Docker daemon
                    sh 'docker --version || echo "Docker CLI not available"'
                    sh 'docker-compose --version || echo "Docker Compose not available"'
                    
                    // Check available disk space
                    sh 'df -h'
                    
                    echo "✅ Environment validation completed"
                }
            }
        }
        
        stage('Build and Test') {
            steps {
                script {
                    echo "🚀 Starting Docker Compose build and test..."
                    
                    try {
                        // Set the project name to avoid conflicts
                        env.COMPOSE_PROJECT_NAME = "pokemon-api-tests-${env.BUILD_NUMBER}"
                        
                        // Build and run the services
                        sh """
                            docker-compose -p ${COMPOSE_PROJECT_NAME} up --build --abort-on-container-exit --exit-code-from api-tests
                        """
                        
                        echo "✅ Tests completed successfully"
                        
                    } catch (Exception e) {
                        echo "❌ Tests failed: ${e.getMessage()}"
                        throw e
                    }
                }
            }
        }
        
        stage('Collect Test Results') {
            steps {
                script {
                    echo "📊 Collecting test results..."
                    
                    // Copy test results from container if they exist
                    sh """
                        docker-compose -p ${COMPOSE_PROJECT_NAME} exec -T api-tests cat /app/test-results.xml || echo "No test results file found"
                    """
                    
                    echo "✅ Test results collection completed"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo " Cleaning up Docker resources..."
                
                // Always clean up containers and networks
                sh """
                    docker-compose -p ${COMPOSE_PROJECT_NAME} down --volumes --remove-orphans || true
                    docker system prune -f || true
                """
                
                echo "✅ Cleanup completed"
            }
        }
        
        success {
            script {
                echo " Pipeline completed successfully!"
            }
        }
        
        failure {
            script {
                echo " Pipeline failed!"
                
                // Capture logs for debugging
                sh """
                    echo "=== Docker Compose Logs ==="
                    docker-compose -p ${COMPOSE_PROJECT_NAME} logs || true
                    
                    echo "=== Container Status ==="
                    docker ps -a || true
                """
            }
        }
        
        cleanup {
            script {
                echo " Final cleanup..."
                
                // Ensure all containers are stopped
                sh """
                    docker-compose -p ${COMPOSE_PROJECT_NAME} down --volumes --remove-orphans || true
                    docker container prune -f || true
                    docker network prune -f || true
                """
            }
        }
    }
}