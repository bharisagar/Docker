# Docker Project Guide

This guide covers fundamental Docker concepts and commands across a four-day learning journey.

---

## Day 1: Docker Basics and Installation

### Topics Covered
- Introduction to Docker — understanding its role as a platform for developing, shipping, and running applications in containers.
- The core benefit of Docker: packaging an application and its dependencies into a standardized unit for software development.
- Docker installation and setup specific to the operating system.
- Verifying the Docker installation by running a simple command.

### Docker Commands Used
```bash
docker --version
docker run hello-world
```

### Evidence
- [Status Page](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/docker-day1-status-page.png)
- [Status Page (Browser View)](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/docker-day1-status-browser-user.png)

---

## Day 2: Docker Images and Containers

### Topics Covered
- Understanding Docker images as lightweight, standalone, executable packages containing code, runtime, libraries, environment variables, and config files.
- Managing Docker containers as runnable instances of an image.
- Running interactive containers to work directly inside a container's OS.
- Listing and inspecting images and containers to view properties and states.
- Stopping and removing containers and images to manage system resources.

### Docker Commands Used
```bash
docker pull <image_name>
docker images
docker run -it ubuntu bash
docker ps
docker ps -a
docker stop <container_id>
docker rm <container_id>
docker rmi <image_id>
```

### Evidence
- [Health API](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/docker-day2-health-api.png)
- [Version API](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/docker-day2-version-api.png)
- [Home Page (Browser View)](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/docker-day2-home-browser-user.png)
- [docker images output](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/docker-terminal-images-user.png)
- [docker ps output](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/docker-terminal-ps-user.png)

---

## Day 3: Dockerfile and Building Custom Images (Multi-stage)

### Topics Covered
- Dockerfile syntax and best practices (`FROM`, `RUN`, `COPY`, `EXPOSE`).
- Building custom Docker images from a Dockerfile.
- Understanding image layers using `docker history`.
- Introduction to multi-stage builds for smaller, more secure images.

### Docker Commands Used
```bash
docker build -t <image_name> .
docker history <image_name>
docker inspect <image_name>
```

### Evidence
- [Container Running](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/day3-container-running.png)
- [First Request](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/day3-first-request.png)
- [Visit Counter](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/day3-visit-counter.png)

---

## Day 4: Docker Volumes and Networking

### Topics Covered
- Managing data persistence with Docker volumes, ensuring data is retained when containers are stopped or removed.
- Understanding Docker networking concepts for inter-container communication.
- Creating and managing custom networks to isolate traffic and enable name-based resolution.
- Connecting multiple containers via a custom network to build multi-service applications.

### Docker Commands Used
```bash
docker volume create myvolume
docker volume ls
docker run -d --name devtest --mount source=myvolume,target=/app nginx
docker inspect devtest
docker network create mynetwork
docker network ls
docker run -d --name mynginx --network mynetwork nginx
docker run -d --name mynode --network mynetwork mynodeimage
docker network inspect mynetwork
```

### Evidence
- [Network Created](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/day4-network-created.png)
- [Network Inspect](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/day4-network-inspect.png)
- [Postgres Container Running](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/day4-postgres-container-running.png)
- [Postgres Data Query](https://github.com/bharisagar/Docker/blob/main/evidence-screenshots/day4-postgres-data-query.png)
