#/bin/bash

export PYTHONPATH=$PYTHONPATH:$PWD
export RUNNING_ENV=local
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

input=$1
if [ "$input" = "--use-dummy-data" ]
then
  sudo mysql -u root -pyour_db_password bara_LS_local < dummy_data.sql # -p와 db_password 사이에 공백이 없어야 함 e.g. -pmy_db_password
  python ./app/main.py --use-dummy-data
elif [ "$input" = "--create-dummy-data" ]
then
  python ./app/main.py --create-dummy-data
else
  python ./app/main.py
fi
