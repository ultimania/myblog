pipeline {
    stages{
        stage(first){
            steps{
                sh '''
                uname -a
                '''
            }
        }
        stage(second){
            steps{
                sh '''
                hostname -i
                '''
            }
        }
    }
}