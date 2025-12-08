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
                    echo ===== Verificando Python =====
                    python --version

                    echo ===== Actualizando pip =====
                    python -m pip install --upgrade pip

                    echo ===== Instalando dependencias =====
                    pip install -r requirement.txt
                '''
            }
        }

        stage('Run App') {
            steps {
                bat '''
                    echo ===== Iniciando Flask en background =====
                    start "" /B python app.py > flask.log 2>&1

                    echo ===== LOGS DE FLASK =====
                    type flask.log
                '''
            }
        }
    }
}