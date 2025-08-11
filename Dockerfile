# Use Python Alpine as base image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Setup timezone
RUN apk add tzdata && \
  cp /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime && \
  echo "Asia/Ho_Chi_Minh" > /etc/timezone

# Install system dependencies
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# Copy dependency files for better layer caching
COPY pyproject.toml ./

# Install dependencies using pip
RUN pip install --no-cache-dir . && \
    pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Expose the port specified in the .env
EXPOSE 6699

# Run the application with gunicorn
CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:6699", "main:app"]
