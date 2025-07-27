FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN echo '#!/bin/bash\n\
echo "Waiting for mock service to be ready..."\n\
timeout 60 bash -c "until curl -f http://mock-service:3001/api/pokemon/pikachu; do sleep 2; done" || exit 1\n\
echo "Mock service is ready! Running tests..."\n\
pytest tests/ -v\n\
' > /app/run-tests.sh && chmod +x /app/run-tests.sh

CMD ["/app/run-tests.sh"]
