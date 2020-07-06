podTemplate(
  label: 'skaffold',
  containers: [
    containerTemplate(name: 'skaffold-insider', image: 'ultimania/skaffold', ttyEnabled: true, command: 'cat')
  ],
  volumes: [
    hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')
  ]
) {
  node('skaffold') {
    withCredentials([
      usernamePassword(credentialsId: 'docker_id', usernameVariable: 'DOCKER_ID_USR', passwordVariable: 'DOCKER_ID_PSW')
    ]) {
      stage('Info') {
        container('skaffold-insider') {
          sh """
            uname -a
            whoami
            pwd
            ls -al
            env
          """
        }
      }
      stage('Image Build & Push by skaffold') {
        git url: 'https://github.com/ultimania/myblog', branch: 'dashboard'
        container('skaffold-insider') {
          sh """
            docker login --username=$DOCKER_ID_USR --password=$DOCKER_ID_PSW
            skaffold run -p release
          """
        }
      }
    }
  }
}