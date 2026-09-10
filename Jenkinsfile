pipeline {
    agent any
    environment {
        IMAGE_NAME = 'python-jenkins-agent:3.12'
        CONTAINER_WORKDIR = '/workspace'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Run Tests in Docker') {
            steps {
                script {
                    bat """
                        docker run --rm ^
                        --entrypoint bash ^
                        -v "%WORKSPACE%:${CONTAINER_WORKDIR}" ^
                        -w ${CONTAINER_WORKDIR} ^
                        ${IMAGE_NAME} ^
                        -c "python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt && pytest -v --html=reports/report.html --self-contained-html --maxfail=1 --disable-warnings"
                    """
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: '**/report.html', allowEmptyArchive: true
        }
    }
}