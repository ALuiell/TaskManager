# 1. Use the base Python image (3.12)
FROM python:3.12-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Upgrade pip and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# 5. Copy project files into the container
COPY . /app

# 6. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 7. Expose the application port (optional)
EXPOSE 8000

# 7. Start the Django application
CMD ["python manage.py runserver 0.0.0.0:8000"]

