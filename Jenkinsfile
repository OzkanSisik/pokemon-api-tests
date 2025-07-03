pipeline {
    agent {
        docker {
            image 'python:3.11'  // pytest yüklü resmi Python image'i kullanabilirsin
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'git@github.com:OzkanSisik/pokemon-api-tests.git',
                    credentialsId: 'bc25183b-cbc9-4ac7-a68c-93808aacb47f',
                    branch: 'main'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pip install pytest'  // image içinde yoksa yükle
                sh 'pytest'
            }
        }
    }
}
