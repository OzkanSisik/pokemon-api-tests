pipeline {
    agent {
        docker {
            image 'python:3.11'   // pytest gibi test araçları için Python resmi image
            args '-v /var/run/docker.sock:/var/run/docker.sock' // opsiyonel, docker komutu kullanacaksan
        }
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'bc25183b-cbc9-4ac7-a68c-93808aacb47f',
                    url: 'git@github.com:OzkanSisik/pokemon-api-tests.git'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pip install pytest'   // Gerekirse test kütüphaneleri yüklenir
                sh 'pytest'               // Testler çalıştırılır
            }
        }
    }
}
