start wsl.exe -e ./run-redis.sh
timeout 5
start CMD /K "h:/Code/Projects/rooaa/venv/Scripts/activate && celery worker -A manage.celery --loglevel=info"
start CMD /K "h:/Code/Projects/rooaa/venv/Scripts/activate && python manage.py"