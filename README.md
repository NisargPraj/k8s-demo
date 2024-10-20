# Flask Blog Application

This project is a Flask-based blog application consisting of a backend and a frontend service, deployed on Kubernetes with Docker.

## Prerequisites

Before running the application, ensure you have the following installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Kubernetes](https://kubernetes.io/docs/setup/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NisargPraj/k8s-demo.git
cd k8s-demo
```

### 2. Create Docker Image

Create frontend and backend images for docker by running:

```bash
docker build -t frontend-flaskblog:latest .
docker build -t backend-flaskblog:latest .
```

### 3. Run the setup-kind.sh script file

Run the script command by moving into the scripts folder and executing the following command:

```bash
./setup-kind.sh
```
