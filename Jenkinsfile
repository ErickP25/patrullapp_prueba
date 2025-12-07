pipeline {
    agent any

    environment {
        PYTHONHOME = "C:/Users/conie/AppData/Local/Programs/Python/Python313"
        PATH = "${env.PYTHONHOME};${env.PYTHONHOME}/Scripts;${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                    echo "Verificando versión de Python..."
                    python --version
                    
                    echo "Actualizando pip..."
                    pip install --upgrade pip
                    
                    echo "Instalando dependencias..."
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            when {
                expression { fileExists('tests') }
            }
            steps {
                sh """
                    echo "Ejecutando pruebas..."
                    pytest || true
                """
            }
        }

        stage('Run App') {
            steps {
                sh """
                    echo "Levantando Flask..."
                    python app.py
                """
            }
        }
    }
}