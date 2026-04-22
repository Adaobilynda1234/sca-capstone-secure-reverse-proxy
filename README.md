# Capstone Project

## Development Branch
This is the development staging branch for the project.

---

## Project Goal:
We are building a secure internal web application (student/admin portal) using Docker, Nginx, HTTPS, CI/CD, and Kubernetes. It will run locally but be designed like a real production system.

### 1. Application (Frontend + Backend + DB)

- Frontend: HTML/CSS (or React if we want)
- Backend: Flask
- Database: MySQL
- Features: Admin dashboard or student portal
- Add /health endpoint

### 2. Nginx Reverse Proxy + TLS

- Configure Nginx as reverse proxy
- Route traffic to app container
- Enable HTTPS using self-signed certificate
- SSL/TLS

### 3. Docker Setup

- Write Dockerfile for app
- Create Docker Compose to connect:
  - nginx
  - app
  - mysql
- Ensure containers communicate properly

### 4. Logging & Monitoring

- Capture:
  - Nginx access logs
  - App logs
- Show evidence (screenshots/log output)
- Add basic metrics or health checks

### 5. CI/CD Pipeline

- Use GitHub Actions
- Build Docker image
- Push image to Docker Hub (or GHCR)

### 6. Kubernetes (Minikube)

- Deploy app using:
  - Pods / Deployments
  - Services
  - Ingress (acts like Nginx in K8s)

### 7. AWS Architecture (Design Only)