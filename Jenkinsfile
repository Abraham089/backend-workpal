
pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
    timeout(time: 30, unit: 'MINUTES')
  }

  environment {
    REGISTRY       = 'ghcr.io'
    IMAGE_NAME     = 'abraham089/backend-workpal'
    POETRY_VERSION = '2.4.1'


    ALGORITHM                   = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = '30'
    FRONTEND_URL                = 'http://localhost:5173'
    FRONTEND_IP_URL             = 'http://127.0.0.1:5173'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install, Test & Audit') {
      agent {
        docker {
          image 'python:3.12-slim'
          reuseNode true
        }
      }
      environment {
        SECRET_KEY                  = credentials('workpal-secret-key')
        HOME                        = "${WORKSPACE}"
        PIP_CACHE_DIR               = "${WORKSPACE}/.cache/pip"
        POETRY_CACHE_DIR            = "${WORKSPACE}/.cache/pypoetry"
        POETRY_VIRTUALENVS_IN_PROJECT = 'true'
        POETRY_INSTALLER_ONLY_BINARY  = ':all:'
      }
      stages {
        stage('Install dependencies') {
          steps {
            sh '''
              python -m venv .poetry
              .poetry/bin/pip install --quiet --only-binary :all: "poetry==${POETRY_VERSION}"
              .poetry/bin/poetry sync --no-interaction
            '''
          }
        }

        stage('Tests + coverage') {
          steps {
            sh '''
              mkdir -p reports
              .poetry/bin/poetry run pytest \
                --junitxml=reports/junit.xml \
                --cov=src/backend_workpal \
                --cov-report=xml:coverage.xml
            '''
          }
          post {
            always {
              junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            }
          }
        }

        stage('Dependency audit') {
          steps {
            sh '.poetry/bin/poetry run pip-audit'
          }
        }
      }
    }

    stage('SonarCloud') {
      agent {
        docker {
          image 'sonarsource/sonar-scanner-cli:latest'
          reuseNode true
        }
      }
      environment {
        SONAR_TOKEN     = credentials('sonar-token')
        SONAR_USER_HOME = "${WORKSPACE}/.sonar"
      }
      steps {
        script {
         
          def args = env.CHANGE_ID
            ? "-Dsonar.pullrequest.key=${env.CHANGE_ID} -Dsonar.pullrequest.branch=${env.CHANGE_BRANCH} -Dsonar.pullrequest.base=${env.CHANGE_TARGET}"
            : "-Dsonar.branch.name=${env.BRANCH_NAME}"
          sh "sonar-scanner -Dsonar.host.url=https://sonarcloud.io ${args}"
        }
      }
    }

    stage('Build & Push image') {
      when {
        anyOf { branch 'main'; branch 'dev' }
      }
      environment {
        GHCR             = credentials('ghcr-credentials')
        ENVIRONMENT_NAME = "${env.BRANCH_NAME == 'main' ? 'production' : 'development'}"
      }
      steps {
        sh '''
          IMAGE="${REGISTRY}/${IMAGE_NAME}"

          echo "$GHCR_PSW" | docker login "$REGISTRY" -u "$GHCR_USR" --password-stdin

          docker build \
            --label org.opencontainers.image.source="https://github.com/${IMAGE_NAME}" \
            --label org.opencontainers.image.revision="${GIT_COMMIT}" \
            -t "${IMAGE}:${ENVIRONMENT_NAME}-${BUILD_NUMBER}" \
            -t "${IMAGE}:${ENVIRONMENT_NAME}-latest" \
            .

          docker push "${IMAGE}:${ENVIRONMENT_NAME}-${BUILD_NUMBER}"
          docker push "${IMAGE}:${ENVIRONMENT_NAME}-latest"
        '''
      }
      post {
        always {
          sh 'docker logout "$REGISTRY" || true'
        }
      }
    }

    // kubernetes/backend_deployment.yaml tenga contenido
  
  }

  post {
    always {
      deleteDir()
    }
  }
}
