pipeline {
    agent any

    environment {
        DOCKER_USER = "gokumonkey"
        TOKEN = "dckr_pat_vHMjHr6LEPU-5_bZln8EdQf_HzY"
        IMAGE_NAME = "order-service"
        DOCKER_SERVER = "ubuntu@13.235.76.142"
    }

    stages {

        stage('Source') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/gokumonkey-36/order-service.git'
            }
        }



        stage('Build Image') {
            steps {
               sh '''
               docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER} .
               '''
            }
        }


        stage('Push Docker Image') {
            steps {
                sh '''
                    docker login -u ${DOCKER_USER} -p ${TOKEN} &&
                    docker push ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }

    }
}
