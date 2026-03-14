FROM python:3.11-slim

WORKDIR /app

# Install system deps (if needed) and python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose port
EXPOSE 5000

ENV FLASK_ENV=production

# Run the Flask app with gunicorn for production
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} app:app
