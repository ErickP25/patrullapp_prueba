pipeline {
    agent any

    environment {
        GIT_CREDENTIALS = credentials('github-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/ErickP25/patrullapp_prueba.git',
                        credentialsId: 'github-token'
                    ]]
                ])
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirement.txt
                '''
            }
        }
        stage('Run App') {
            steps {
                bat 'python main.py'
            }
        }
    }
}