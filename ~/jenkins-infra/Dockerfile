FROM jenkins/jenkins:lts

USER root

# Install Docker CLI and Compose
RUN apt-get update \
    && apt-get install -y docker.io docker-compose \
    && rm -rf /var/lib/apt/lists/*

# Add Jenkins user to the 'staff' group (GID 20 on macOS for Docker socket access)
RUN groupadd -g 20 staff || true \
    && usermod -aG staff jenkins

USER jenkins 