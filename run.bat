start bash -c -i "cd redis-stable && src/redis-server"
timeout 5
start bash -c -i "source linux-venv/bin/activate && celery worker -A manage.celery --loglevel=info"
start bash -c -i "source linux-venv/bin/activate && python manage.py"