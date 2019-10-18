REM Run on WSL 

REM start bash -c -i "cd redis-stable && src/redis-server"
REM timeout 5
REM start bash -c -i "source linux-venv/bin/activate && celery worker -A rooaa.extensions:celery -l info"
REM start bash -c -i "source linux-venv/bin/activate && python manage.py -p"

REM Run on Windows instead..

start CMD /K bash -c -i "cd redis-stable && src/redis-server"
timeout 5
start CMD /K "celery worker -A rooaa.extensions:celery -l info"
python manage.py -p