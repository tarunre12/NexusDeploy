pipeline {
    agent any

    environment {
        IMAGE_NAME = "nexusdeploy-app"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install & Unit Test') {
            steps {
                dir('app') {
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt'
                    sh '. venv/bin/activate && pytest -v'
                }
            }
        }

        stage('Docker Build') {
            steps {
                dir('app') {
                    sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                }
            }
        }

        stage('Docker Push') {
            steps {
                echo "Push stage will be added in Phase 3 once ECR is set up"
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded"
        }
        failure {
            echo "Pipeline failed — check the stage logs above"
        }
    }
}