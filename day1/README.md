# Docker Day 1 Notes

Containers, architecture, installation, images, containers, and Docker Hub.

## Topics Covered

1. What Docker is and why it exists
2. The problem Docker solves
3. Virtual machines vs containers
4. Docker architecture: Client, Host, Daemon, Registry
5. Docker image vs Docker container
6. Docker installation
7. Docker Hub as a public image registry
8. Day 1 practice project
9. Interview questions

## 1. What Is Docker?

Docker is a software platform used to create, run, and deploy applications using containers.

A container packages an application together with everything it needs:

- Application code
- Runtime
- Libraries
- Dependencies
- Configuration

The goal is simple: the same application should run the same way on a developer laptop, testing server, production server, or cloud VM.

## 2. The Problem Docker Solves

Classic problem:

```text
Developer: It works on my machine.
Tester: It does not work on my machine.
```

This happens because different machines may have:

- Different operating system versions
- Different library versions
- Different environment variables
- Different runtime versions
- Different configurations

Docker solves this by packaging the app and its environment into one container.

Result:

- Same code
- Same dependency versions
- Same runtime
- Same behavior across environments

## 3. Virtual Machines vs Containers

| Virtual Machine | Docker Container |
| --- | --- |
| Has its own full operating system | Shares the host OS kernel |
| Runs on a hypervisor | Runs on Docker Engine |
| Heavy, often GBs in size | Lightweight, often MBs in size |
| Takes minutes to boot | Starts in seconds |
| Strong OS-level isolation | Process-level isolation |
| Good for full OS environments | Good for apps, microservices, and CI/CD |

Simple analogy:

- VM: A full house for each tenant
- Container: An apartment inside one building

Containers share the building infrastructure, but each container has its own isolated space.

## 4. Docker Architecture

Docker uses a client-server architecture.

### Docker Client

The Docker Client is the interface you use from the terminal.

Examples:

```bash
docker run nginx
docker build -t myapp:v1 .
docker pull ubuntu:22.04
```

The client sends commands to the Docker Daemon.

### Docker Daemon

The Docker Daemon is the background service that does the real work.

It is also called `dockerd`.

It manages:

- Images
- Containers
- Networks
- Volumes

### Docker Host

The Docker Host is the machine where Docker is installed and running.

It can be:

- Your laptop
- A Linux server
- An EC2 instance
- A cloud VM

### Docker Registry

A Docker Registry stores Docker images.

Common registries:

- Docker Hub
- AWS ECR
- GitHub Container Registry
- Google Artifact Registry

Docker Hub is the default public registry.

### Architecture Flow

```text
User terminal
    |
    v
Docker Client
    |
    v
Docker Daemon on Docker Host
    |
    |-- local images
    |-- running containers
    |
    v
Docker Registry, such as Docker Hub
```

Example flow:

1. You run `docker run nginx`.
2. Docker Client sends the request to Docker Daemon.
3. Docker Daemon checks whether the `nginx` image exists locally.
4. If not, Docker pulls it from Docker Hub.
5. Docker creates and starts a container from that image.

## 5. Docker Image vs Docker Container

| Docker Image | Docker Container |
| --- | --- |
| Blueprint or template | Running instance of an image |
| Read-only | Read-write runtime layer |
| Stored on disk | Runs as a process |
| Built from a Dockerfile | Created using `docker run` |
| One image can create many containers | Each container is independent |

Simple analogy:

- Image: Recipe
- Container: Dish made from the recipe

One image can create many containers.

## 6. Docker Image Layers

Docker images are made of layers.

Each instruction in a Dockerfile creates a new layer.

Example:

```text
Layer 1: Base OS
Layer 2: Install packages
Layer 3: Copy application files
Layer 4: Set startup command
```

Docker caches unchanged layers. This makes future builds faster.

## 7. Install Docker

### Ubuntu / Linux Installation

```bash
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
```

Add Docker GPG key:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Add Docker repository:

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker:

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

Start and enable Docker:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

Verify:

```bash
docker --version
docker info
```

### Quick Practice Install

Use this only in practice environments:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

Log out and log back in, then run:

```bash
docker run hello-world
```

### Windows / Mac

Install Docker Desktop:

```text
https://www.docker.com/products/docker-desktop
```

Windows requires WSL2. Docker Desktop usually sets it up during installation.

Verify:

```bash
docker --version
docker run hello-world
```

## 8. Docker Hub

Docker Hub is the default public registry for Docker images.

Think of Docker Hub as GitHub for Docker images.

Popular official images:

- `nginx`
- `ubuntu`
- `python`
- `node`
- `mysql`
- `redis`

Common commands:

```bash
docker pull nginx
docker pull nginx:1.25
docker pull ubuntu:22.04
docker pull python:3.11-slim
docker search nginx
docker login
docker push yourusername/myapp:v1.0
```

## 9. Day 1 Project: Install And Verify Docker

For the complete real-time project, open:

[Day 1 Real-Time Project: Deploy An Incident Status Page With Docker Hub](./real-time-project/README.md)

### Goal

Install Docker and prove that the Docker Client, Docker Daemon, and Docker Hub flow are working.

### Tasks

1. Install Docker on your machine or Ubuntu EC2 instance.
2. Verify the Docker CLI:

```bash
docker --version
```

3. Verify the Docker Daemon:

```bash
docker info
```

4. Run the hello-world container:

```bash
docker run hello-world
```

5. Pull an image from Docker Hub:

```bash
docker pull nginx
```

6. Run nginx:

```bash
docker run -d -p 8080:80 --name day1-nginx nginx
```

7. Check running containers:

```bash
docker ps
```

8. Open the app:

```text
http://localhost:8080
```

For EC2:

```text
http://<EC2_PUBLIC_IP>:8080
```

9. Clean up:

```bash
docker stop day1-nginx
docker rm day1-nginx
```

### Expected Evidence

Submit screenshots or terminal output for:

- `docker --version`
- `docker info`
- `docker run hello-world`
- `docker ps` showing nginx running
- Browser showing nginx page

## 10. Interview Questions

### Q1. What is Docker and why is it used?

Docker is a platform for building, running, and deploying applications in containers. It packages an application with its dependencies so it runs consistently across environments.

### Q2. What is the difference between a VM and a container?

A VM includes a full operating system and runs on a hypervisor. A container shares the host OS kernel, is lighter, starts faster, and is better suited for application packaging and DevOps pipelines.

### Q3. Explain Docker architecture.

Docker architecture includes:

- Docker Client: CLI used by the user
- Docker Daemon: background service that manages Docker objects
- Docker Host: machine where Docker runs
- Docker Registry: stores images, such as Docker Hub

### Q4. What is the difference between an image and a container?

An image is a read-only template. A container is a running instance of that image.

### Q5. What is Docker Hub?

Docker Hub is the default public registry where Docker images are stored, pulled, and shared.

### Q6. What is the difference between `docker run` and `docker start`?

`docker run` creates a new container from an image and starts it.

`docker start` starts an existing stopped container.

## Summary

By the end of Day 1, you should understand:

- Why Docker exists
- How Docker solves environment mismatch
- VM vs container differences
- Docker architecture
- Image vs container
- Docker installation and verification
- Docker Hub basics
