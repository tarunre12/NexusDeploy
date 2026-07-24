pipeline {
    agent any

    environment {
        IMAGE_NAME = "nexusdeploy-app"
        ECR_REPO = "469351852174.dkr.ecr.us-east-1.amazonaws.com/nexusdeploy"
        AWS_REGION = "us-east-1"
    }

    stages {
        stage('ECR Login') {
            steps {
                sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}"
            }
        }

        stage('Docker Build & Tag') {
            steps {
                dir('app') {
                    sh "docker build -t ${ECR_REPO}:latest -t ${ECR_REPO}:${GIT_COMMIT} ."
                }
            }
        }

        stage('Docker Push') {
            steps {
                sh "docker push ${ECR_REPO}:latest"
                sh "docker push ${ECR_REPO}:${GIT_COMMIT}"
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                sh "aws eks update-kubeconfig --name nexusdeploy --region ${AWS_REGION}"
                sh "helm upgrade --install nexusdeploy nexusdeploy-chart --set image.tag=${GIT_COMMIT}"
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