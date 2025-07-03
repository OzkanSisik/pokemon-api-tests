#!/bin/bash

echo "Setting up Jenkins with Docker access on macOS..."

# Stop and remove existing Jenkins container
echo "Stopping existing Jenkins container..."
docker stop jenkins 2>/dev/null || true
docker rm jenkins 2>/dev/null || true

# Create Jenkins container with Docker access (macOS version)
echo "Creating Jenkins container..."
docker run -d --name jenkins \
  -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  -v ~/.jenkins_ssh:/var/jenkins_home/.ssh:ro \
  jenkins/jenkins:lts

# Wait for Jenkins to start
echo "Waiting for Jenkins to start..."
sleep 15

# Test Docker access from Jenkins container
echo "Testing Docker access from Jenkins container..."
docker exec jenkins docker --version

if [ $? -eq 0 ]; then
    echo "SUCCESS: Jenkins can access Docker successfully!"
    echo "Jenkins is available at: http://localhost:8080"
    echo "Initial admin password:"
    docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
else
    echo "ERROR: Jenkins cannot access Docker."
    echo "This might be a macOS Docker Desktop permission issue."
    echo "Try running: docker exec jenkins groups"
fi
