pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE = 'rnafezai/counter-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh 'docker run --rm --volumes-from jenkins -w "$WORKSPACE" python:3.12-alpine sh -c "pip install -q --root-user-action=ignore --disable-pip-version-check -r requirements.txt -r requirements-test.txt && pytest -v -p no:cacheprovider"'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .'
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                                  usernameVariable: 'DOCKERHUB_USER',
                                                  passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh 'echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin'
                    sh 'docker push $IMAGE:$BUILD_NUMBER'
                    sh 'docker push $IMAGE:latest'
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
        success {
            echo 'Pipeline OK: image published on Docker Hub'
        }
        failure {
            echo 'Pipeline FAILED: see the stage in red'
        }
    }
}
