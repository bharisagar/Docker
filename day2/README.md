# Docker Day 2 Notes

Dockerfile instructions, image builds, command behavior, and container management commands.

## Topics Covered

1. What a Dockerfile is
2. Dockerfile instructions: `FROM`, `RUN`, `EXPOSE`, `CMD`, `ENTRYPOINT`, `COPY`, `ADD`, `ARG`
3. `CMD` vs `ENTRYPOINT`
4. `COPY` vs `ADD`
5. Complete Dockerfile example for a Python web app
6. Container commands: `exec`, `logs`, `ps`, `inspect`, `stop`, `pause`, `kill`, `rm`
7. `stop` vs `kill` vs `pause`
8. Day 2 projects and homework
9. Interview questions

## 1. What Is A Dockerfile?

A Dockerfile is a plain text file that contains instructions to build a custom Docker image.

Docker reads the Dockerfile from top to bottom and creates the image layer by layer.

Important points:

- A Dockerfile has no file extension.
- The file name should be exactly `Dockerfile`.
- Each instruction creates a read-only image layer.
- Layers are cached and reused when unchanged.
- You use `docker build` to convert a Dockerfile into an image.

Flow:

```text
Dockerfile -> docker build -> Docker Image -> docker run -> Docker Container
```

Simple analogy:

- Dockerfile: Recipe
- Docker image: Cooked package
- Docker container: Running application

## 2. What Is A Base Image?

A base image is the starting point of your custom Docker image.

Every Dockerfile usually starts with `FROM`.

Examples:

```dockerfile
FROM ubuntu:22.04
FROM python:3.11-slim
FROM node:18-alpine
FROM nginx:alpine
```

Best practices:

- Use official images when possible.
- Pin versions instead of using `latest` in production.
- Choose the smallest base image that meets your needs.
- Smaller images are faster to pull and have less attack surface.

## 3. Dockerfile Instructions

### FROM

`FROM` defines the base image.

It is usually the first instruction in the Dockerfile.

Syntax:

```dockerfile
FROM <image>:<tag>
```

Examples:

```dockerfile
FROM ubuntu:22.04
FROM python:3.11-slim
FROM node:18-alpine
FROM nginx:alpine
```

Best practice:

```dockerfile
FROM python:3.11-slim
```

Avoid this in production:

```dockerfile
FROM python:latest
```

### RUN

`RUN` executes commands during the image build process.

Use it to:

- Install packages
- Update dependencies
- Create directories
- Set permissions
- Configure the image

Examples:

```dockerfile
RUN apt-get update
RUN apt-get install -y curl wget git
```

Better layer practice:

```dockerfile
RUN apt-get update && \
    apt-get install -y curl wget git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

Key point:

- `RUN` happens during `docker build`.
- The result is saved inside the image.

### EXPOSE

`EXPOSE` documents which port the container listens on.

Example:

```dockerfile
EXPOSE 8080
```

Important:

`EXPOSE` does not publish the port to your host machine.

To access the port from outside the container, use `-p`:

```bash
docker run -p 8080:8080 myapp
```

Meaning:

```text
host port 8080 -> container port 8080
```

### CMD

`CMD` defines the default command that runs when the container starts.

Recommended exec form:

```dockerfile
CMD ["python", "app.py"]
CMD ["node", "server.js"]
CMD ["nginx", "-g", "daemon off;"]
```

Shell form:

```dockerfile
CMD python app.py
```

Important:

- Only the last `CMD` in a Dockerfile is used.
- `CMD` can be overridden from `docker run`.

Example:

```bash
docker run myimage bash
```

This overrides the Dockerfile `CMD`.

### ENTRYPOINT

`ENTRYPOINT` defines a fixed command that runs when the container starts.

Example:

```dockerfile
ENTRYPOINT ["python", "app.py"]
```

`ENTRYPOINT` is useful when the container should behave like a specific executable.

Example with `ENTRYPOINT` and `CMD`:

```dockerfile
ENTRYPOINT ["grep"]
CMD ["-n", "error"]
```

Default run:

```bash
docker run myimage
```

Runs:

```bash
grep -n error
```

Override arguments:

```bash
docker run myimage -v root
```

Runs:

```bash
grep -v root
```

### CMD vs ENTRYPOINT

| CMD | ENTRYPOINT |
| --- | --- |
| Provides a default command | Provides a fixed command |
| Easy to override | Not easily overridden |
| Good for flexible containers | Good for executable-style containers |
| Only last CMD is used | Works well with CMD as default arguments |

Use `CMD` when the container should have a default behavior but remain flexible.

Use `ENTRYPOINT` when the container should always run a specific command.

Use both when you need a fixed command with default arguments.

### COPY

`COPY` copies files and directories from your build context into the image.

Examples:

```dockerfile
COPY app.py /app/app.py
COPY ./src /app/src
COPY . /app
COPY requirements.txt package.json /app/
```

Best practice for dependency caching:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

This allows Docker to reuse the dependency layer when only application code changes.

### ADD

`ADD` is similar to `COPY`, but has extra behavior:

- Can download files from URLs
- Automatically extracts local tar archives

Examples:

```dockerfile
ADD app.tar.gz /app/
ADD https://example.com/config.zip /config/
ADD config.json /app/config.json
```

### COPY vs ADD

| COPY | ADD |
| --- | --- |
| Copies local files/directories | Copies files and has extra features |
| Simple and predictable | Can auto-extract archives |
| Preferred for normal use | Use only when needed |
| Best for app source code | Best for tar extraction or URL download |

Best practice:

Use `COPY` by default.

Use `ADD` only when you need its special features.

### ARG

`ARG` defines build-time variables.

These variables are available only during image build.

Examples:

```dockerfile
ARG VERSION=1.0
ARG APP_ENV=production
ARG APP_PORT=8080
```

Use with:

```dockerfile
ARG APP_PORT=8080
EXPOSE ${APP_PORT}
```

Pass values during build:

```bash
docker build --build-arg VERSION=2.0 -t myapp:v2 .
docker build --build-arg APP_ENV=staging -t myapp:staging .
```

Important:

- `ARG` is available during build only.
- `ARG` is not available in the running container.
- Do not use `ARG` for secrets or passwords.

Use:

- `ARG` for build flags and versions
- `ENV` for runtime configuration
- Docker secrets or runtime environment files for secrets

## 4. Complete Dockerfile Example: Python Web App

Project files:

```text
python-web-app/
  app.py
  requirements.txt
  Dockerfile
```

Example `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Docker Python web app"

@app.route("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Example `requirements.txt`:

```text
flask==3.0.0
```

Example `Dockerfile`:

```dockerfile
FROM python:3.11-slim

ARG APP_VERSION=1.0
ARG APP_ENV=production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "app.py"]
```

Build:

```bash
docker build -t myapp:v1.0 .
```

Build with ARG:

```bash
docker build --build-arg APP_VERSION=2.0 -t myapp:v2.0 .
```

Run:

```bash
docker run -d -p 5000:5000 --name myapp myapp:v1.0
```

Verify:

```bash
docker ps
docker logs myapp
```

Open:

```text
http://localhost:5000
```

## 5. Docker Container Commands

### Login To A Running Container

```bash
docker exec -it <container_id> bash
```

If `bash` is not available:

```bash
docker exec -it <container_id> sh
```

Run one command inside a container:

```bash
docker exec <container_id> ls -la /app
docker exec <container_id> cat /etc/nginx/nginx.conf
```

Meaning:

- `-i`: interactive
- `-t`: pseudo-terminal

### Logs

```bash
docker logs <container_id>
docker container logs --details <container_id>
docker logs -f <container_id>
docker logs --tail 50 <container_id>
docker logs -t <container_id>
```

### Processes And Resource Usage

```bash
docker top <container_id>
docker stats
docker stats <container_id>
```

### List Containers And Images

```bash
docker ps
docker ps -a
docker images
```

### Inspect

Inspect an image or container:

```bash
docker inspect <image_id>
docker inspect <container_id>
```

Get specific fields:

```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' <container_id>
docker inspect --format='{{.State.Status}}' <container_id>
```

### Start, Stop, Restart

```bash
docker stop <container_id>
docker start <container_id>
docker restart <container_id>
```

### Pause, Unpause, Kill

```bash
docker pause <container_id>
docker unpause <container_id>
docker kill <container_id>
```

### Remove Containers And Images

Remove a stopped container:

```bash
docker rm <container_id>
```

Force remove a running container:

```bash
docker rm -f <container_id>
```

Remove all stopped containers:

```bash
docker container prune
```

Remove an image:

```bash
docker rmi <image_id>
docker rmi nginx:latest
```

## 6. stop vs kill vs pause

| Command | Behavior | Use Case |
| --- | --- | --- |
| `docker stop` | Sends SIGTERM, waits, then SIGKILL if needed | Normal production shutdown |
| `docker kill` | Sends SIGKILL immediately | Container is stuck or unresponsive |
| `docker pause` | Freezes all processes using SIGSTOP | Temporarily stop CPU usage |
| `docker rm` | Deletes stopped container record | Cleanup |

Best practice:

- Use `docker stop` first.
- Use `docker kill` only when graceful stop fails.
- Use `docker pause` when you want to freeze and resume later.
- Use `docker rm` only when you no longer need the container.

## 7. Command Reference Table

| Command | What It Does |
| --- | --- |
| `docker exec -it <id> bash` | Open interactive shell inside container |
| `docker logs <id>` | View container logs |
| `docker logs -f <id>` | Follow logs in real time |
| `docker images` | List local images |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker inspect <id>` | Show full JSON details |
| `docker stop <id>` | Gracefully stop a container |
| `docker start <id>` | Start a stopped container |
| `docker restart <id>` | Restart a container |
| `docker pause <id>` | Freeze container processes |
| `docker unpause <id>` | Resume paused container |
| `docker kill <id>` | Force kill immediately |
| `docker rm <id>` | Remove stopped container |
| `docker rm -f <id>` | Force remove running container |
| `docker rmi <image>` | Remove image |
| `docker top <id>` | Show processes inside container |
| `docker stats` | Show live CPU/memory usage |
| `docker container prune` | Remove stopped containers |

## 8. Day 2 Project: Build Your First Custom Image

### Goal

Build a custom nginx image, run it, inspect it, and practice container lifecycle commands.

### Step 1: Create Project Folder

```bash
mkdir dockerfile-practice
cd dockerfile-practice
```

### Step 2: Create HTML App

```bash
echo '<h1>Hello from my Docker image! Built by YourName</h1>' > index.html
```

### Step 3: Create Dockerfile

```bash
nano Dockerfile
```

Add:

```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Step 4: Build Image

```bash
docker build -t my-web:v1 .
docker images
```

### Step 5: Run Container

```bash
docker run -d -p 8080:80 --name my-web my-web:v1
docker ps
```

Open:

```text
http://localhost:8080
```

For EC2:

```text
http://<EC2_PUBLIC_IP>:8080
```

### Step 6: Practice Commands

```bash
docker logs my-web
docker exec -it my-web sh
docker top my-web
docker inspect my-web
docker pause my-web
docker ps
docker unpause my-web
docker stop my-web
docker rm my-web
```

### Expected Evidence

Submit:

- `docker images` showing `my-web:v1`
- `docker ps` showing the running container
- Browser screenshot of the custom page
- `docker logs my-web`
- `docker inspect my-web`
- Cleanup output after `docker rm`

## 9. Homework

### Task 1: Python App Dockerfile

Create `hello.py`:

```python
print("Hello from Docker!")
```

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY hello.py .
CMD ["python", "hello.py"]
```

Build:

```bash
docker build -t hello-python:v1 .
```

Run:

```bash
docker run --name hello hello-python:v1
```

### Task 2: Practice Container Commands

Run nginx:

```bash
docker run -d -p 9090:80 --name test-nginx nginx
```

Practice:

```bash
docker logs test-nginx
docker exec -it test-nginx sh
docker top test-nginx
docker inspect test-nginx
docker pause test-nginx
docker unpause test-nginx
docker stop test-nginx
docker rm test-nginx
docker ps -a
```

### Task 3: Use ARG In Dockerfile

Example:

```dockerfile
FROM alpine:3.19
ARG MY_NAME=YourName
RUN echo "Built by ${MY_NAME}"
CMD ["sh", "-c", "echo Container started"]
```

Build:

```bash
docker build --build-arg MY_NAME=BariSagar -t arg-test .
```

Expected evidence:

- Screenshot or terminal output showing the build output with your name

## 10. Interview Questions

### Q1. What is a Dockerfile?

A Dockerfile is a plain text file containing instructions to build a Docker image. Docker reads it top to bottom and creates image layers.

### Q2. What is the difference between CMD and ENTRYPOINT?

`CMD` gives a default command and can be overridden.

`ENTRYPOINT` defines a fixed command that always runs unless overridden with `--entrypoint`.

### Q3. What is the difference between COPY and ADD?

`COPY` copies local files and directories.

`ADD` can also download URLs and auto-extract tar archives.

Best practice: use `COPY` unless you specifically need `ADD`.

### Q4. What is the difference between RUN and CMD?

`RUN` executes during image build and becomes part of the image.

`CMD` executes when the container starts.

### Q5. What is the difference between docker stop and docker kill?

`docker stop` sends SIGTERM first and allows graceful shutdown.

`docker kill` sends SIGKILL immediately with no cleanup time.

### Q6. What does docker pause do?

`docker pause` freezes all processes inside the container. `docker unpause` resumes them from the same state.

### Q7. What is ARG in a Dockerfile?

`ARG` defines build-time variables passed using `docker build --build-arg`. ARG values do not persist as runtime container variables.

### Q8. What does docker inspect do?

`docker inspect` returns detailed JSON information about a container or image, including networking, mounts, config, environment, and state.

## Summary

By the end of Day 2, you should be able to:

- Write a Dockerfile
- Explain key Dockerfile instructions
- Build custom Docker images
- Run containers from custom images
- Debug containers using logs, exec, inspect, top, and stats
- Stop, kill, pause, remove, and clean up containers safely
