# Pokemon API Tests

A Python-based container networking test project that demonstrates multi-container communication using Docker Compose.

## What it does

This project demonstrates how to run integration tests in isolated containers that communicate over Docker networks. The main goal is to test container-to-container communication patterns, not the API itself. 

The setup consists of two separate containers:
- **Mock Service Container**: Runs a Node.js mock API server
- **Test Container**: Runs Python tests that make requests to the mock service

Both containers communicate over a custom Docker network, simulating real-world microservice architectures where services need to discover and communicate with each other.

**Note**: This project uses Docker socket mounting (`/var/run/docker.sock`) rather than Docker-in-Docker (DinD), which is more efficient and follows industry best practices for CI/CD environments. No host port mapping is used for security. Still much more to improve tho! :)

## Project Structure

```
├── api/                 # API client code
├── tests/              # Test files
├── config/             # Configuration settings
│   └── settings.py     # Environment configuration
├── docker-compose.yml  # Container orchestration
├── Dockerfile          # Container definition
├── Jenkinsfile         # CI/CD pipeline
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── .dockerignore      # Docker ignore rules
└── README.md          # Project documentation
```

## Quick Start

### Prerequisites
- Docker installed (includes Docker Compose)

### Running Tests

The easiest way to run tests is using Docker Compose:

```bash
# Run all tests
docker-compose up --abort-on-container-exit --exit-code-from api-tests
```

This will:
1. Pull the mock service from Docker Hub
2. Pull the test container from Docker Hub  
3. Start both containers
4. Wait for mock service to be ready
5. Run the test suite
6. Clean up containers and networks automatically

### Accessing the Mock Service

I didn't expose the mock service port to keep things simple and follow container best practices. If you need to access it directly:

**Option 1**: Access the mock service repository directly: [pokemon-mock-service](https://github.com/OzkanSisik/pokemon-mock-service)

**Option 2**: Add port mapping to docker-compose.yml:
```yaml
mock-service:
  image: ozkansisik/mock-pokemon-api:latest
  ports:
    - "3001:3001"  # Expose for local access
```

## Test Coverage

The test suite includes:
- Pokemon data retrieval tests
- Error handling for invalid requests
- API response validation

## CI/CD

This project is configured to run in Jenkins CI. The pipeline:
- Pulls latest images from Docker Hub
- Runs tests in isolated containers
- Reports results and cleans up resources

## Docker Images

- **Mock Service**: `ozkansisik/mock-pokemon-api:latest`
- **Test Container**: `ozkansisik/pokemon-api-tests:latest`
```
