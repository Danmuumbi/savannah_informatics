# frontend/Dockerfile


FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

WORKDIR /app


COPY requirements.txt .


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .


ENV PYTHONPATH=/app:$PYTHONPATH

# Create a volume or directory for static files 
RUN mkdir -p /vol/static


EXPOSE 8000

WORKDIR /app


CMD sh -c "python -m gunicorn frontend.wsgi:application --bind 0.0.0.0:$PORT --workers 3"