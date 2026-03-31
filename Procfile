web: ./release.sh && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60
worker: celery -A config worker --loglevel=info
beat: celery -A config beat --loglevel=info
