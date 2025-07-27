pipeline {
    agent any
    
    environment {
        // Future use: For image versioning when we implement build process
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        COMPOSE_PROJECT_NAME = "pokemon-api-tests-${env.BUILD_NUMBER}"
    }
    
    options {
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
        
        stage('Pull Latest Images') {
            steps {
                script {
                    echo "📦 Pulling latest images from Docker Hub..."
                    
                    // Pull all images defined in docker-compose.yml
                    sh "docker-compose pull"
                    
                    echo "✅ Images pulled successfully"
                }
            }
        }
        
        stage('Build and Test') {
            steps {
                script {
                    echo "🚀 Starting Docker Compose build and test..."
                    
                    try {
                        env.COMPOSE_PROJECT_NAME = "pokemon-api-tests-${env.BUILD_NUMBER}"
                        
                        sh """
                            docker-compose -p ${COMPOSE_PROJECT_NAME} up --abort-on-container-exit --exit-code-from api-tests
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
                echo "🧹 Cleaning up Docker resources..."
                
                sh """
                    docker-compose -p ${COMPOSE_PROJECT_NAME} down --volumes --remove-orphans || true
                    docker system prune -f || true
                """
                
                echo "✅ Cleanup completed"
            }
        }
        
        success {
            script {
                echo "✅ Pipeline completed successfully!"
            }
        }
        
        failure {
            script {
                echo "❌ Pipeline failed!"
                
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
                echo "🧹 Final cleanup..."
                
                sh """
                    docker-compose -p ${COMPOSE_PROJECT_NAME} down --volumes --remove-orphans || true
                    docker container prune -f || true
                    docker network prune -f || true
                """
        }
    }
}
}