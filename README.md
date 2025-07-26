# Pokemon API Tests

A Python-based API testing project that runs integration tests against a mock Pokemon API service.

## What it does

This project contains automated tests for a Pokemon API. The tests run against a mock service that simulates a real Pokemon API, allowing us to test our API integration without depending on external services.

## Project Structure

```
├── api/                 # API client code
├── tests/              # Test files
├── config/             # Configuration settings
├── docker-compose.yml  # Container orchestration
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development)

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
4. Run the test suite
5. Clean up automatically


## Test Coverage

The test suite covers:
- Pokemon data retrieval
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


## Notes

- The mock service runs separately and is pulled from Docker Hub
- Tests use container networking for communication
- No host port mapping is used for security
