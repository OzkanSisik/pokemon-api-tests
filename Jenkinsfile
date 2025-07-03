pipeline {
    agent any
    
    environment {
        // Define environment variables for the pipeline
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        WORKSPACE_CLEAN = "${env.WORKSPACE}"
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
                    // Clean workspace before checkout
                    cleanWs()
                    
                    echo "🔍 Checking out repository..."
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
        
        stage('Validate Environment') {
            steps {
                script {
                    echo "�� Validating Jenkins environment..."
                    
                    // Check if Docker is available
                    sh 'docker --version'
                    
                    // Check if Docker Compose is available
                    sh 'docker-compose --version'
                    
                    // Check available disk space
                    sh 'df -h'
                    
                    // Check Docker daemon status
                    sh 'docker info'
                    
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
                    
                    // Publish test results if available
                    publishTestResults testResultsPattern: '**/test-results.xml', allowEmptyResults: true
                    
                    echo "✅ Test results collection completed"
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "�� Cleaning up Docker resources..."
                
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
                echo "�� Pipeline completed successfully!"
                
                // Optional: Send success notification
                // emailext (
                //     subject: "✅ Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                //     body: "Build ${env.BUILD_NUMBER} completed successfully.",
                //     to: "your-email@example.com"
                // )
            }
        }
        
        failure {
            script {
                echo "�� Pipeline failed!"
                
                // Capture logs for debugging
                sh """
                    echo "=== Docker Compose Logs ==="
                    docker-compose -p ${COMPOSE_PROJECT_NAME} logs || true
                    
                    echo "=== Container Status ==="
                    docker ps -a || true
                """
                
                // Optional: Send failure notification
                // emailext (
                //     subject: "❌ Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                //     body: "Build ${env.BUILD_NUMBER} failed. Check Jenkins for details.",
                //     to: "your-email@example.com"
                // )
            }
        }
        
        cleanup {
            script {
                echo "�� Final cleanup..."
                
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