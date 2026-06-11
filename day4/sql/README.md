# Docker Day 4 - Volumes, Networks, Docker System Commands and .dockerignore

## Overview

In Day 4, we explored some of the most important Docker concepts used in real-world DevOps projects.

Until Day 3, we learned how to:

* Run Containers
* Create Docker Images
* Build Custom Images using Dockerfile
* Multi-Stage Docker Builds
* Docker Compose

However, one important challenge still exists.

What happens if a Database Container is deleted?

Without persistent storage, all database data will be lost.

To solve this problem, Docker provides **Volumes**.

Another challenge is communication between containers.

For example:

* Application Container → Database Container
* Backend Container → Redis Container
* Frontend Container → Backend Container

To solve this problem, Docker provides **Networks**.

In this practical session, we implemented:

* Docker Volume
* Docker Network
* PostgreSQL Database Container
* SQL Initialization Script
* Container-to-Container Communication
* Docker DNS
* Network Inspection
* Docker System Commands
* .dockerignore Concepts

---

# Learning Objectives

By the end of this practical, students will understand:

* What is a Docker Volume
* Why Docker Volumes are needed
* What is a Docker Network
* How containers communicate
* What is Docker DNS
* How PostgreSQL works inside Docker
* Data Persistence
* Network Inspection
* Docker System Commands
* .dockerignore

---

# Real-World Problem

Imagine a PostgreSQL database running inside a Docker container.

Without Docker Volume:

```text
Container Deleted
        ↓
Database Deleted
        ↓
Data Lost
```

This is unacceptable in production environments.

Docker solves this problem using Volumes.

With Docker Volume:

```text
Container Deleted
        ↓
Volume Exists
        ↓
Data Preserved
```

This is how databases are managed in production.

---

# Project Architecture

## Volume Architecture

```text
+-----------------------------+
| PostgreSQL Container        |
| postgres-db                |
+-------------+---------------+
              |
              |
              |
              V
+-----------------------------+
| Docker Volume               |
| postgres-data              |
+-----------------------------+
```

Database files are stored inside the Docker Volume instead of inside the container.

---

## Network Architecture

```text
+-----------------------------+
| PostgreSQL Client Container |
+-------------+---------------+
              |
              |
              |
              V
+-----------------------------+
| PostgreSQL Database         |
| postgres-db                |
+-----------------------------+

Connected through:

day4-network
```

Containers communicate using Docker Network.

---

# Folder Structure

```text
Docker/
│
├── day4/
│   ├── sql/
│   │   └── init.sql
│   ├── notes.txt
│   └── README.md
│
└── evidence-screenshots/
    ├── day4-network-created.png
    ├── day4-volume-created.png
    ├── day4-postgres-container-running.png
    ├── day4-postgres-data-query.png
    └── day4-network-inspect.png
```

---

# What is Docker Volume?

A Docker Volume is a storage mechanism used to persist container data outside the container lifecycle.

Without Volume:

```text
Container Removed
       ↓
Data Lost
```

With Volume:

```text
Container Removed
       ↓
Data Preserved
```

Volumes are commonly used with:

* PostgreSQL
* MySQL
* MongoDB
* Redis
* Elasticsearch

---

# Step 1 - Create Docker Network

Create a custom Docker Network.

```bash
docker network create day4-network
```

Verify:

```bash
docker network ls
```

Purpose:

* Allows container communication
* Provides Docker DNS
* Enables Service Discovery

---

# Evidence - Docker Network Created

![Docker Network Created](../evidence-screenshots/day4-network-created.png)

The custom network named:

```text
day4-network
```

was successfully created.

---

# Step 2 - Create Docker Volume

Create Docker Volume.

```bash
docker volume create postgres-data
```

Verify:

```bash
docker volume ls
```

Purpose:

* Store PostgreSQL Database Files
* Preserve data across container recreation
* Provide persistent storage

---

# Evidence - Docker Volume Created

![Docker Volume Created](../evidence-screenshots/day4-volume-created.png)

The volume named:

```text
postgres-data
```

was successfully created.

---

# Step 3 - SQL Initialization Script

File:

```text
sql/init.sql
```

Contents:

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    course VARCHAR(100)
);

INSERT INTO students (name, course) VALUES
('Chetan','Computer Science'),
('Manjunath','Mathematics'),
('Suresh','Physics');
```

Purpose:

* Automatically create table
* Automatically insert sample data
* Demonstrate persistence

---

# Step 4 - Run PostgreSQL Container

Command:

```bash
docker run -d \
--name postgres-db \
--network day4-network \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=admin123 \
-e POSTGRES_DB=studentdb \
-v postgres-data:/var/lib/postgresql/data \
-v /c/bari_sagar/Docker/day4/sql/init.sql:/docker-entrypoint-initdb.d/init.sql \
-p 5432:5432 \
postgres:15
```

Explanation:

| Parameter | Description                 |
| --------- | --------------------------- |
| --name    | Container Name              |
| --network | Attach Container to Network |
| -e        | Environment Variables       |
| -v        | Volume Mount                |
| -p        | Port Mapping                |

---

# Evidence - PostgreSQL Container Running

![PostgreSQL Running](../evidence-screenshots/day4-postgres-container-running.png)

Verification:

```bash
docker ps
```

The PostgreSQL container started successfully and exposed port:

```text
5432
```

---

# Step 5 - Connect to PostgreSQL from Another Container

Instead of connecting directly from the host machine, we launched a PostgreSQL Client Container.

```bash
docker run -it --rm \
--network day4-network \
postgres:15 \
psql -h postgres-db -U admin -d studentdb
```

Password:

```text
admin123
```

Important Observation:

Notice the hostname:

```text
postgres-db
```

This is the Container Name.

No IP Address is required.

Docker automatically resolves:

```text
postgres-db
```

to the correct container IP.

This feature is called **Docker DNS**.

---

# Step 6 - Query Database Records

Run:

```sql
SELECT * FROM students;
```

Output:

```text
 id | name      | course
----+-----------+-------------------
 1  | Chetan    | Computer Science
 2  | Manjunath | Mathematics
 3  | Suresh    | Physics
```

---

# Evidence - Query Results

![PostgreSQL Query](../evidence-screenshots/day4-postgres-data-query.png)

This confirms:

* PostgreSQL is running
* Network communication works
* SQL script executed successfully
* Docker DNS is functioning

---

# What is Docker DNS?

Docker automatically creates DNS entries for containers connected to the same network.

Example:

```text
Application Container
        |
        |
        V
postgres-db
```

Instead of using:

```text
172.18.0.5
```

we can simply use:

```text
postgres-db
```

Docker automatically resolves the container name.

This feature is called:

```text
Service Discovery
```

---

# Step 7 - Inspect Docker Network

Command:

```bash
docker network inspect day4-network
```

Purpose:

* View connected containers
* View subnet information
* View IP allocation

---

# Evidence - Docker Network Inspection

![Docker Network Inspection](../evidence-screenshots/day4-network-inspect.png)

The output shows:

* Network Driver
* Subnet Configuration
* Connected Containers
* IP Address Allocation

---

# What is .dockerignore?

The `.dockerignore` file is used to exclude unnecessary files from Docker build context.

Example:

```text
.git
*.log
.env
node_modules
__pycache__
```

Benefits:

* Faster Builds
* Smaller Images
* Improved Security
* Reduced Storage Usage

---

# Docker System Commands

## Check Docker Disk Usage

```bash
docker system df
```

Displays:

* Images
* Containers
* Volumes
* Build Cache

---

## List Running Containers

```bash
docker ps
```

---

## List All Containers

```bash
docker ps -a
```

---

## List Volumes

```bash
docker volume ls
```

---

## List Networks

```bash
docker network ls
```

---

## Remove Stopped Containers

```bash
docker container prune
```

---

## Remove Unused Images

```bash
docker image prune
```

---

## Remove Unused Volumes

```bash
docker volume prune
```

---

## Remove Unused Networks

```bash
docker network prune
```

---

## Complete Docker Cleanup

```bash
docker system prune -a --volumes
```

⚠ Warning:

This command removes:

* Containers
* Images
* Networks
* Volumes
* Build Cache

Use carefully.

---

# Real-World Use Cases

Docker Volumes are used for:

* PostgreSQL
* MySQL
* MongoDB
* Redis
* Elasticsearch

Docker Networks are used for:

* Frontend to Backend Communication
* Backend to Database Communication
* Backend to Redis Communication
* Microservices Communication

Example:

```text
Frontend
    |
    V
Backend API
    |
    V
PostgreSQL
```

All services communicate through Docker Networks.

---

# Interview Questions

## What is Docker Volume?

A Docker Volume is a persistent storage mechanism used to store container data outside the container lifecycle.

---

## Why do we need Docker Volumes?

Volumes ensure data remains available even after containers are deleted or recreated.

---

## What is Docker Network?

A Docker Network enables communication between containers.

---

## How do containers communicate?

Containers communicate using container names through Docker DNS.

Example:

```text
postgres-db
```

instead of IP addresses.

---

## What is Docker DNS?

Docker DNS automatically resolves container names into IP addresses.

---

## What is Service Discovery?

Service Discovery is the ability of containers to find and communicate with other containers using names instead of IP addresses.

---

## What is the difference between Bridge and Host Network?

Bridge Network:

* Default Docker Network
* Isolated Container Networking

Host Network:

* Shares Host Networking Stack
* No Network Isolation

---

## What is .dockerignore?

A file used to exclude files and directories from Docker build context.

---

# Learning Outcomes

By completing Day 4, we successfully learned:

* Docker Volumes
* Persistent Storage
* PostgreSQL Database Container
* Docker Networks
* Docker DNS
* Service Discovery
* Container Communication
* SQL Initialization
* Network Inspection
* Docker System Commands
* .dockerignore

These concepts are heavily used in production Docker environments and form the foundation for Kubernetes Persistent Volumes, Services, and Networking.

---

# Conclusion

In this practical session, we successfully created a PostgreSQL Database Container using Docker Volumes and Docker Networks.

We demonstrated how data can be stored persistently using Docker Volumes and how containers can communicate using Docker Networks without requiring manual IP configuration.

These concepts are fundamental for designing scalable, reliable, and production-ready containerized applications.
