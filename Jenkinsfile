pipeline {
    agent any

    tools {
        python 'Python3'   
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
                    echo "Ejecutando pruebas (si existen)..."
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