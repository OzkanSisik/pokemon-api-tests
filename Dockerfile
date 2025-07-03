FROM python:3.11-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create a script to wait for mock service and run tests
RUN echo '#!/bin/bash\n\
echo "Waiting for mock service to be ready..."\n\
timeout 60 bash -c "until curl -f http://mock-service:3001/api/pokemon/pikachu; do sleep 2; done" || exit 1\n\
echo "Mock service is ready! Running tests..."\n\
pytest tests/ -v\n\
' > /app/run-tests.sh && chmod +x /app/run-tests.sh

# Default command
CMD ["/app/run-tests.sh"]
