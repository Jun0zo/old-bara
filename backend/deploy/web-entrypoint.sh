echo "Waiting for DB server..."
dockerize -wait tcp://db:3306 -timeout 30s
python /app/prod_init.py
bash /start.sh