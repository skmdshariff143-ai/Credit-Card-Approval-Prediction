# Docker Containerization Guide

This guide explains how to build, run, and orchestrate the containerized CreditGuard AI service.

---

## 1. Image Optimizations
- **Base Layer**: Built on Python 3.10-slim to reduce image sizes to less than 200MB.
- **Security Check**: Disables root execution. Uses a non-root system user (`appuser` with UID 999) inside the container.
- **Multistage Build**: Installs dev tools (`build-essential`) in a builder stage and copies only compiled packages to the runner.

---

## 2. Docker CLI Commands
Build the container image:
```bash
docker build -t credit-card-approval-prediction:latest .
```

Run the container instance:
```bash
docker run -d -p 5000:5000 --env-file .env --name credit_card_container credit-card-approval-prediction:latest
```

---

## 3. Docker Compose Orchestration
Manage container orchestration using docker-compose:
- Start services:
  ```bash
  docker-compose up -d
  ```
- Stop services:
  ```bash
  docker-compose down
  ```
- Check logs:
  ```bash
  docker-compose logs -f
  ```
