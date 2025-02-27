pipeline {
    agent any

    environment {
        REPO_URL = "git@github.com:PratikKr10/kubernetes_with_jenkins.git"
        WORKDIR = "${WORKSPACE}/my-k8s-app"
        VENV_PATH = "${WORKSPACE}/venv"
        DOCKER_IMAGE = "my-k8s-app:latest"
        K8S_NAMESPACE = "k8s-demo"
    }

    stages {
        stage('Clone Repository') {
            steps {
                cleanWs()
                sh '''
                    echo "Cloning repository..."
                    if [ -d "$WORKDIR" ]; then
                        rm -rf "$WORKDIR"
                    fi
                    git clone $REPO_URL "$WORKDIR"
                    echo "Repository cloned successfully!"
                    ls -la "$WORKDIR"
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv "$VENV_PATH"
                . "$VENV_PATH/bin/activate"
                pip install --upgrade pip build pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Checking current working directory...'
                    sh 'pwd'

                    echo 'Listing files before changing directory...'
                    sh 'ls -la'

                    echo 'Changing directory to app...'
                    sh 'cd my-k8s-app/app && ls -la'

                    echo 'Building Docker Image...'
                    sh 'cd my-k8s-app/app && docker build -t my-k8s-app:latest .'
                }
            }
        }




        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f "$WORKDIR/k8s/namespace.yaml"
                kubectl apply -f "$WORKDIR/k8s/configmap.yaml"
                kubectl apply -f "$WORKDIR/k8s/deployment.yaml"
                kubectl apply -f "$WORKDIR/k8s/service.yaml"
                kubectl -n $K8S_NAMESPACE rollout status deployment/flask-app
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs.'
        }
    }
}

