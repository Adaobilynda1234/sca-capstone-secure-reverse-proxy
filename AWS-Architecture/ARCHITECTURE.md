# AWS Capstone Architecture: Reverse Proxy and TLS Internal Portal

## Project Overview

This project demonstrates a secure internal portal architecture built using **Docker**, **NGINX**, **Kubernetes (Minikube)**, **GitHub Actions**, and **AWS services**.

The application was containerized and deployed inside a private AWS environment while exposing secure HTTPS access through an **Application Load Balancer (ALB)**.

### Main Goals

- Implement NGINX reverse proxying  
- Configure TLS/HTTPS encryption  
- Separate frontend, backend, and database services  
- Deploy containers with Minikube  
- Implement CI/CD using GitHub Actions  
- Collect logs and monitoring metrics  
- Design a secure AWS cloud architecture  

---

## Architecture Overview

The architecture is divided into:

- A public subnet for internet-facing services  
- Private subnets for application and database resources  

Users access the application securely through **HTTPS (port 443)**.

Traffic flow:

1. User → HTTPS → ALB  
2. ALB performs TLS termination using AWS Certificate Manager (ACM)  
3. ALB re-encrypts traffic  
4. Traffic is forwarded to NGINX (inside private Minikube)  
5. NGINX performs second TLS termination (self-signed certificate)  
6. Requests are routed to:
   - Frontend service  
   - Flask backend service  

The backend application communicates securely with an **Amazon RDS MySQL database** located in a separate private subnet.

---

## Networking and Security

The architecture uses a **Virtual Private Cloud (VPC)** with multiple subnets to isolate resources and improve security.

### Public Subnet

Contains:

- Application Load Balancer (ALB)  
- NAT Gateway  

The ALB receives public HTTPS traffic from the internet, while the NAT Gateway allows private resources to access the internet securely for updates, package downloads, and container image pulls.

---

### Private Application Subnet

Contains:

- EC2 instance  
- Docker runtime  
- Minikube cluster  
- NGINX reverse proxy  
- Frontend pod  
- Backend pod  

> The EC2 instance is intentionally placed in a private subnet to prevent direct public access.

---

### Private Database Subnet

- Amazon RDS (MySQL)  
- Isolated from external access  

---

### Security Controls

**Security Groups:**

- Only HTTPS traffic from the ALB is allowed into the application layer  
- Only backend services can access the MySQL database on port 3306  

**Network ACLs:**

- Provide additional subnet-level traffic filtering  

---

## Reverse Proxy and TLS Flow

NGINX acts as the reverse proxy for the application. It receives requests from the ALB and routes traffic to the frontend and backend services running inside Minikube.

### TLS Stages

#### Leg 1 — Public TLS
User → HTTPS → ALB
- The ALB terminates the external HTTPS connection  

#### Leg 2 — Internal TLS
ALB → HTTPS (Re-encrypted) → NGINX
- Traffic is re-encrypted by the ALB  
- NGINX performs the second TLS termination using a self-signed certificate  

This design demonstrates secure layered communication between public and private application tiers.

---

## Kubernetes and Containerization

Docker was used to containerize:

- NGINX  
- Frontend service  
- Flask backend service  

Minikube was deployed on the EC2 instance to simulate a Kubernetes environment. The application components run as Kubernetes pods inside the cluster.

### Health Endpoint
/health

Used for:

- Health monitoring  
- Service validation  

---

## Monitoring and Logging

### Amazon CloudWatch

Used for:

- Application logs  
- Metrics  
- Alarms  
- Monitoring  

NGINX logs and Flask application logs are forwarded to CloudWatch for observability.

---

### AWS CloudTrail

Records AWS API activity such as:

- IAM actions  
- Resource operations  
- Account events  

---

### VPC Flow Logs

Capture:

- Accepted traffic  
- Rejected traffic  
- Network metadata  

---

### Storage

- Logs and monitoring artifacts are stored in **Amazon S3**  

---

## CI/CD Pipeline

The CI/CD workflow was implemented using **GitHub Actions**.

### Pipeline Flow

GitHub Repository
→ GitHub Actions
→ Build & Test Docker Images
→ Push to Docker Hub
→ Deploy to EC2/Minikube


This automates container builds and deployment processes.

---

## Administrative Access

Because the EC2 instance resides in a private subnet, **AWS Systems Manager Session Manager** was used for secure administration instead of exposing SSH access publicly.

> This eliminates the need for public SSH ports and improves security.

---

## Conclusion

This project successfully demonstrates:

- NGINX reverse proxy implementation  
- TLS encryption and re-encryption  
- Docker containerization  
- Kubernetes deployment using Minikube  
- Secure AWS networking  
- Monitoring and logging  
- CI/CD automation using GitHub Actions  

---

## Summary

This architecture provides a practical demonstration of modern cloud-native deployment and security concepts using AWS infrastructure and container technologies.