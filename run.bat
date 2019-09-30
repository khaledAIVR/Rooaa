REM Run on WSL 

REM start bash -c -i "cd redis-stable && src/redis-server"
REM timeout 5
REM start bash -c -i "source linux-venv/bin/activate && celery worker -A manage:celery -l info -f celery.log"
REM start bash -c -i "source linux-venv/bin/activate && python manage.py"

REM Run on Windows instead..

start CMD /K bash -c -i "cd redis-stable && src/redis-server"
timeout 5
start CMD /K "celery worker -A manage:celery -l info -f celery.log"
python manage.py