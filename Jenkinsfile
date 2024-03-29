pipeline {
    agent any
    environment {
       tgBot_id = credentials('recipeBot_id')
       recipeBot_postgres_pass = credentials('recipeBot_postgres_pass')
       recipeBot_postgres_login = credentials('recipeBot_postgres_login')
       db_location = credentials('db_location')
       CHAT_ID = credentials('my_chat_id')
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