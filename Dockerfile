FROM python:3.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

# Expose le port 8000
EXPOSE 8000

# shell Linux  commande  gunicorn exécute notre application  0.0.0.0 = aucune addresse défini  -- nb travailleurs <= au nombre de processeurs

CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]