FROM python:3.9-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# collectstatic loads the Django settings, which require a SECRET_KEY.
# This build-only value is not stored in the image: the real key is provided
# at runtime through the environment (Render).
RUN SECRET_KEY=build-only-collectstatic python manage.py collectstatic --noinput

# Default port for local use (Render provides its own through $PORT)
EXPOSE 8000

# Start Gunicorn through a shell so that $PORT is expanded (falls back to 8000).
# 0.0.0.0 listens on every network interface of the container.
# Keep the number of workers at or below the number of available CPUs.
CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2"]