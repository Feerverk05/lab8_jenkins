// CI Pipeline: Checkout -> Static Code Analysis -> Install Dependencies -> Run UI Tests -> Allure Report
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)                         // код отримуємо в окремому етапі Checkout
        timeout(time: 20, unit: 'MINUTES')                // збірка не «зависне» назавжди
        buildDiscarder(logRotator(numToKeepStr: '20'))    // зберігати 20 останніх збірок
    }

    triggers {
        pollSCM('H/5 * * * *')    // кожні ~5 хв перевіряти, чи є нові коміти в репозиторії
    }

    environment {
        REPO_URL = 'https://github.com/Feerverk05/lab8_jenkins'
        VENV     = '.venv'                   // віртуальне середовище в робочій папці збірки
        HEADLESS = 'true'          // браузер без графічного інтерфейсу
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Static Code Analysis') {
            steps {
                // Quality Gate: якщо оцінка Pylint < 8.0 (fail-under у pyproject.toml), збірка зупиняється тут
                sh '''
                    python3 -m venv "$VENV"
                    "$VENV/bin/pip" install --quiet --upgrade pip pylint
                    "$VENV/bin/pylint" features pages config.py --output-format=text:pylint-report.txt,text
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '"$VENV/bin/pip" install --quiet -r requirements.txt'
            }
        }

        stage('Run UI Tests') {
            steps {
                script {
                    // Якщо тести впадуть, збірка стане UNSTABLE, але звіт усе одно буде створено
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        sh '''
                            rm -rf allure-results
                            "$VENV/bin/behave" -f allure_behave.formatter:AllureFormatter -o allure-results -f pretty
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            // Відомості про середовище для блоку Environment у звіті Allure
            sh '''
                mkdir -p allure-results
                {
                    echo "Browser=$(chromium --version)"
                    echo "Python=$(python3 --version)"
                    echo "Base.URL=https://www.saucedemo.com/"
                    echo "Headless=$HEADLESS"
                } > allure-results/environment.properties
            '''
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            archiveArtifacts artifacts: 'pylint-report.txt', allowEmptyArchive: true
        }
        success  { echo 'Pipeline passed: усі етапи успішні.' }
        unstable { echo 'Pipeline unstable: частина тестів не пройшла, див. Allure Report.' }
        failure  { echo 'Pipeline failed.' }
    }
}
