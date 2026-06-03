pipeline{
    agent any
    environment{
        DOCKER_USER ='gokumonkey'
        TOKEN = "dckr_pat_vHMjHr6LEPU-5_bZln8EdQf_HzY"
        IMAGE_NAME = "order-service"
    }
    stages{
        stage('Source'){
            steps{
                git branch: 'main',
                    url: 'https://github.com/gokumonkey-36/order-service.git'
                stash name: 'source', includes: '**/*'
            }
        }

        stage('Build Image'){
            steps{
                sh '''
            docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER} .
            '''
            }
        }

        stage('Push Image'){
            steps{
               sh '''
            docker login -u ${DOCKER_USER} -p ${TOKEN}
            docker push ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER}
            '''  
            }
        }

        stage('Deploy'){
            agent {
                label 'Server'
            }
            steps{
                unstash 'source'

                 sh '''
                kubectl apply -f deployment.yaml
                '''
            }
           
        }
    }
}
