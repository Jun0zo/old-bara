#/bin/bash

export PYTHONPATH=$PYTHONPATH:$PWD
export RUNNING_ENV=test
export SERVER_URL=https://example.com
export SERVICE_NAME="OO운수 사내 시스템"
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_ROOT_PASSWORD=your_db_password
export MYSQL_DATABASE=db_name
export JWT_SECRET=Some_Random_String # openssl rand -hex 32
export JWT_ALGORITHM=HS256
export JWT_ACCESS_TOKEN_EXPIRES=3600
export JWT_REFRESH_TOKEN_EXPIRES=2592000
export GMAIL_ADDR=gmail_addr@gmail.com
export SUPERUSER_EMAIL=superuser@example.com
export SUPERUSER_PW=superuser_password
export SUPERUSER_NAME=superuser_name
export SUPERUSER_ROLE=superuser_role

pytest ./app/tests/test_dashboard.py -vv
pytest ./app/tests/test_transaction.py -vv
pytest ./app/tests/test_user.py -vv
pytest ./app/tests/test_user_role.py -vv
