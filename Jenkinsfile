pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'git@github.com:OzkanSisik/pokemon-api-tests.git', credentialsId: 'bc25183b-cbc9-4ac7-a68c-93808aacb47f'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }
    }
}
