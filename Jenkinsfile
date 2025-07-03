pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'git@github.com:OzkanSisik/pokemon-api-tests.git',
                 credentialsId: '3ce1955f-a763-43ac-b74a-66c82d434b6e',
                 branch: 'main'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }
    }
}
