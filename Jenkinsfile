pipeline {
    agent any
    environment {
       tgBot_id = credentials('vpn_bot_id')
       my_chat_id = credentials('my_chat_id')
       PAYMENT_TOKEN = credentials('PAYMENT_TOKEN')
       FINLAND_1_API_URL = credentials('FINLAND_1_API_URL')
    }
    options {
        retry(3) 
    }
    stages {
       stage('get dependencies'){
            steps {
                sh 'python3 -m venv ./venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
                   }
        }
       stage('runBot'){
            steps {
                sh 'python3 main.py'
                   }
        }
    }

    post {
    failure {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${my_chat_id} -d parse_mode=markdown -d text="*${env.JOB_NAME}* FAILED ${env.BUILD_URL}"
    """)
    }
    aborted {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${my_chat_id} -d parse_mode=markdown -d text="*${env.JOB_NAME}* ABORTED ${env.BUILD_URL}"
    """)
    }

        }
    }