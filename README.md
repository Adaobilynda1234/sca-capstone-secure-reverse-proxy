# Capstone Project

## Project Goal:
We are building a secure internal web application (student/admin portal) using Docker, Nginx, HTTPS, CI/CD, and Kubernetes. It will run locally but be designed like a real production system.

1. Application (Frontend + Backend + DB)

- Frontend: HTML/CSS (or React if we want)
- Backend: Flask
- Database: MySQL
- Features:admin dashboard or student Portal.
- Add /health endpoint

2. Nginx Reverse Proxy + TLS

- Configure Nginx as reverse proxy
- Route traffic to app container
- Enable HTTPS using self-signed certificate
-  SSL/TLS 

3. Docker Setup

- Write Dockerfile for app
- Create Docker Compose to connect:
  - nginx
  - app
  - mysql
- Ensure containers communicate properly

4. Logging & Monitoring

- Capture:
  - Nginx access logs
  - App logs
- Show evidence (screenshots/log output)
- Add basic metrics or health checks.

5. CI/CD Pipeline

- Use GitHub Actions
- Build Docker image
- Push image to Docker Hub (or GHCR)

6. Kubernetes (Minikube)

- Deploy app using:
  - Pods / Deployments
  - Services
  - Ingress (acts like Nginx in K8s)

7. AWS Architecture (Design Only)




## Project Overview

This project builds a **secure internal web application** (Student Records Portal) running behind an Nginx reverse proxy with HTTPS, containerised with Docker, monitored with Prometheus metrics, and deployed to Kubernetes. It is designed to mirror a real production system architecture.

The project is based on the [`docker/awesome-compose` nginx-flask-mysql sample](https://github.com/docker/awesome-compose) and rebranded into a fully functional Student Records Portal.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML/CSS (served via Flask templates) |
| Backend | Python · Flask |
| Database | MySQL |
| Reverse Proxy | Nginx |
| TLS | Self-signed certificate (HTTPS local) |
| Containerisation | Docker · Docker Compose |
| Monitoring | Prometheus client (`/metrics`) · `/health` endpoint |
| CI/CD | GitHub Actions |
| Orchestration | Kubernetes (Minikube) |
| Cloud Design | AWS (EC2 · ALB · S3 · IAM · Security Groups) |

---

## What I Modified

### Before — Original Sample App

The starting point was the `docker/awesome-compose` nginx-flask-mysql sample. It was a plain Flask hello-world app with no database interaction, no styling, and no monitoring.

![Original sample app before modification](screenshots/app-before.png)

---

### After — Student Records Portal

The app was rebranded and extended into a **Student Records Portal** with the following changes:

- Connected Flask to MySQL and seeds a `students` table on startup
- Homepage (`/`) displays student records (name + course) in styled cards
- Password read securely from a Docker secret at `/run/secrets/db-password`
- Added `/health` endpoint returning `{"status": "ok"}`
- Added `/metrics` endpoint with Prometheus request counter

![Student Records Portal after modification](screenshots/app-home.png)

---

**Key changes made to the app:**

- Connected to MySQL and creates a `students` table on startup with seeded records (Ada, John, Mary, David)
- Homepage (`/`) displays student name and course in styled cards
- Reads the database password securely from a Docker secret file at `/run/secrets/db-password`
- Added a **`/health`** endpoint returning `{"status": "ok"}` with HTTP 200
- Added a **`/metrics`** endpoint exposing Prometheus-compatible metrics (total HTTP request count)
- Integrated `prometheus_client` with a `REQUEST_COUNT` counter that increments on every request

```python
# Key endpoints added
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}
```
## Health & Metrics Endpoints

### /health

Returns a simple JSON health check — confirms the app is running:

![/health endpoint response](screenshots/health-endpoint.png)

### /metrics

Exposes Prometheus-compatible metrics including the `request_count` counter:

![/metrics endpoint Prometheus output](screenshots/metrics-endpoint.png)


## Project Structure

```
.
├── backend/
│   ├── hello.py              # Flask app — Student Records Portal
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # App dockerfile
├── proxy/
│   ├── conf            # Nginx reverse proxy config
│   └── Dockerfile/                # dockerfile for Nginx
├── docker-compose.yml   #docker compose
├── db        #database folder
|    ├── password.txt        
├── screenshots/              # Evidence screenshots
│   ├── app-home.png
│   ├── health-endpoint.png
│   ├── metrics-endpoint.png
│   ├── app-before.png
│   
└── README.md
```



---

## How to Run Locally

### Prerequisites
- Docker Desktop installed and running
- `docker compose` available

### Steps

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <project-folder>

# 2. Build and start all containers
docker compose up --build

# 3. Access the app
# HTTP  → redirected to HTTPS
# HTTPS → https://localhost (accept the self-signed cert warning)

# 4. Test endpoints
curl -k https://localhost/health
curl -k https://localhost/metrics

# 5. View proxy logs
docker compose logs proxy

# 6. Stop everything
docker compose down
```

# TASK 2
## Reverse Proxy & TLS Implementation

This project implements a secure internal portal using *Nginx as a reverse proxy with TLS termination*, ensuring that all client traffic is encrypted and routed through a single controlled entry point.

###  Architecture Overview

Client → HTTPS → Nginx (Reverse Proxy) → Backend (Flask App) → Database (MariaDB)

* *Nginx* handles incoming requests and terminates TLS (HTTPS)
* *Flask backend* serves application logic internally
* *MariaDB* stores application data
* Backend and database are isolated within Docker networks

###  Reverse Proxy Configuration

Nginx is configured to act as a reverse proxy, forwarding all incoming requests to the backend service:

* All external traffic is routed through Nginx
* Backend service is not directly exposed to the host
* Internal communication occurs via Docker service networking (backend:8000)

###  TLS (HTTPS) Setup

HTTPS is enabled using a *self-signed SSL certificate* for local development and testing.

#### Key Features:

* TLS termination at the Nginx layer
* Support for modern protocols: *TLSv1.2 and TLSv1.3*
* Secure request handling between client and proxy

#### Certificate Configuration:


ssl_certificate:     /etc/nginx/certs/nginx.crt;
ssl_certificate_key: /etc/nginx/certs/nginx.key;


---

### 🔄 HTTP to HTTPS Redirection

All HTTP traffic is automatically redirected to HTTPS to enforce secure communication:


HTTP (port 80) → 301 Redirect → HTTPS (port 443)


This ensures that users cannot access the application over an insecure connection.

---

### 🛡️ Security Enhancements

Additional security headers are configured in Nginx:

* X-Frame-Options → Prevents clickjacking
* X-Content-Type-Options → Prevents MIME sniffing
* X-XSS-Protection → Enables browser XSS filtering

---

### 🧪 Verification & Testing

The HTTPS setup was validated using the following methods:

#### ✔ Browser Verification

* Application accessible via: https://localhost
* Browser displays secure connection (self-signed warning expected)

#### ✔ HTTP Redirect Test

bash
curl -I http://localhost


Expected:


HTTP/1.1 301 Moved Permanently
Location: https://localhost/


#### ✔ HTTPS Response Test

bash
curl -k -I https://localhost


Expected:


HTTP/1.1 200 OK


#### ✔ Nginx Logs

Requests are successfully routed through Nginx, confirmed via container logs:

bash
docker-compose logs proxy


#### ✔ Certificate Presence

bash
docker-compose exec proxy ls /etc/nginx/certs


---

### 🔒 Security Design Decisions

* Backend service is *not exposed publicly* (no direct port mapping)
* All access is controlled through Nginx
* TLS is terminated at the proxy layer, mimicking real-world production architecture
* Internal services communicate over isolated Docker networks

---

### ✅ Outcome

This implementation ensures:

* Secure HTTPS communication
* Centralized traffic routing via reverse proxy
* Proper service isolation
* Production-aligned architecture design






## References

- [docker/awesome-compose nginx-flask-mysql](https://github.com/docker/awesome-compose/tree/master/nginx-flask-mysql)
- [gh640/docker-compose-depends_on-nginx-certs-sample](https://github.com/gh640/docker-compose-depends_on-nginx-certs-sample)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [Flask Documentation](https://flask.palletsprojects.com/)



