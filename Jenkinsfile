pipeline {
    agent any

    environment {
        KUBECONFIG = "/home/pratik/.kube/config"
    }

    stages {
        stage('Start Minikube') {
            steps {
                script {
                    echo "🚀 Ensuring Minikube is running..."
                    def status = sh(script: "minikube status | grep 'host: Running' || echo 'not running'", returnStdout: true).trim()
                    if (status == "not running") {
                        sh 'minikube stop || true'
                        sh 'minikube delete || true'
                        sh 'minikube start --driver=docker'
                    }
                    sh 'eval $(minikube docker-env)' // Use Minikube's Docker daemon
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "🐳 Building Docker Image..."
                    sh '''
                        eval $(minikube docker-env)
                        cd app
                        docker build -t my-k8s-app:latest .
                        cd ..
                    '''
                }
            }
        }

        stage('Load Image into Minikube') {
            steps {
                script {
                    echo "📦 Loading Docker Image into Minikube..."
                    sh '''
                        eval $(minikube docker-env)
                        minikube image load my-k8s-app:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "🛠 Applying Kubernetes resources..."
                    sh '''
                        kubectl apply -f k8s/namespace.yaml
                        kubectl apply -f k8s/configmap.yaml
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                    '''
                }
            }
        }

        stage('Wait for Deployment') {
            steps {
                script {
                    echo "⏳ Waiting for pods to be ready..."
                    sh 'kubectl -n demo-namespace rollout status deployment/flask-app'
                }
            }
        }

        stage('Get Service URL') {
            steps {
                script {
                    echo "🔗 Retrieving service URL..."
                    sh 'minikube service flask-service -n demo-namespace --url'
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed! Check logs."
        }
    }
}
