I'll give this in a format you can directly copy into `day4/README.md`.

# Docker Day 4 - Volumes, Networks, Docker System Commands and .dockerignore

## Overview

In Day 4, we explored some of the most important Docker concepts used in real-world DevOps projects.

Until Day 3, we learned how to:

* Run containers
* Build custom images
* Create multi-stage Docker builds
* Use Docker Compose

However, one major challenge still exists.

What happens if a database container is deleted?

Without persistent storage, all data inside the container is lost.

To solve this problem, Docker provides **Volumes**.

Another important requirement in containerized applications is communication between containers. For example:

* Application Container → Database Container
* Frontend Container → Backend Container
* Backend Container → Redis Container

To enable this communication, Docker provides **Networks**.

In this practical session, we created:

* Docker Network
* Docker Volume
* PostgreSQL Database Container
* SQL Initialization Script
* Database Persistence Demonstration
* Container-to-Container Communication
* Network Inspection
* Docker Cleanup Commands
* .dockerignore Concepts

---

# Learning Objectives

By the end of this practical, students will understand:

* What Docker Volumes are
* Why Volumes are required
* What Docker Networks are
* How Containers Communicate
* What Docker DNS is
* How PostgreSQL works inside Docker
* How to persist database data
* How to inspect networks and volumes
* What .dockerignore is
* Docker system cleanup commands

---

# Real-World Scenario

Imagine a PostgreSQL database running inside a Docker container.

Without a Docker Volume:

```text
Container Deleted
       ↓
Database Deleted
       ↓
All Data Lost
```

This is unacceptable in production environments.

To solve this issue, Docker provides Volumes.

With Docker Volume:

```text
Container Deleted
       ↓
Volume Remains
       ↓
Data Preserved
```

This is exactly how production databases are managed.

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

Containers communicate using the network.

---

# Folder Structure

```text
day4/
│
├── sql/
│   └── init.sql
│
├── notes.txt
│
└── README.md
```

---

# What is a Docker Volume?

A Docker Volume is a persistent storage mechanism used to store container data outside the container lifecycle.

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

Command:

```bash
docker network create day4-network
```

Verify:

```bash
docker network ls
```

Purpose:

* Allows container communication
* Provides service discovery
* Provides built-in Docker DNS

---

# Evidence - Docker Network Created

![Docker Network Created](../evidence-screenshots/day4-network-created.png)

The network named:

```text
day4-network
```

was successfully created.

---

# Step 2 - Create Docker Volume

Create Docker Volume.

Command:

```bash
docker volume create postgres-data
```

Verify:

```bash
docker volume ls
```

Purpose:

* Store PostgreSQL database files
* Persist data after container deletion

---

# Evidence - Docker Volume Created

![Docker Volume Created](../evidence-screenshots/day4-volume-created.png)

The volume:

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
* Automatically insert records
* Demonstrate data persistence

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

Output confirms:

* PostgreSQL container is running
* Port 5432 is exposed
* Network attachment successful

---

# Step 5 - Connect to Database from Another Container

Instead of connecting directly from the host machine, we launched a PostgreSQL client container.

Command:

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

This is the container name.

No IP address is used.

Docker automatically resolves:

```text
postgres-db
```

to the container IP using Docker DNS.

---

# Step 6 - Query Database Records

Command:

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

* PostgreSQL database is running
* Network communication works
* SQL script executed successfully
* Docker DNS is functioning correctly

---

# What is Docker DNS?

Docker provides built-in DNS resolution.

When containers are attached to the same network:

```text
Container A
      |
      |
      V
Container B
```

Container A can access Container B using:

```text
container-name
```

instead of:

```text
172.x.x.x
```

Example:

```text
postgres-db
```

Docker automatically resolves this hostname.

This feature is called Docker Service Discovery.

---

# Step 7 - Inspect Docker Network

Command:

```bash
docker network inspect day4-network
```

Purpose:

* View connected containers
* View subnet configuration
* View allocated IP addresses

---

# Evidence - Docker Network Inspection

![Docker Network Inspect](../evidence-screenshots/day4-network-inspect.png)

The output shows:

* Network Driver
* IPAM Configuration
* Assigned Subnet
* Connected Containers

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

## List Docker Volumes

```bash
docker volume ls
```

---

## List Docker Networks

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

Warning:

This command removes:

* Containers
* Images
* Volumes
* Networks
* Build Cache

Use carefully.

---

# Real-World Use Cases

Docker Volumes are used for:

* PostgreSQL Databases
* MySQL Databases
* MongoDB Databases
* Redis Data Storage
* Elasticsearch Data

Docker Networks are used for:

* Microservices Communication
* Frontend to Backend Communication
* Backend to Database Communication
* Application to Cache Communication

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

## What is a Docker Volume?

A Docker Volume is a persistent storage mechanism used to store container data outside the container lifecycle.

---

## Why do we need Docker Volumes?

Volumes ensure data remains available even after containers are deleted or recreated.

---

## What is a Docker Network?

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

## What is the difference between Bridge and Host Network?

Bridge Network:

* Default Docker Network
* Isolated Networking

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
* PostgreSQL in Docker
* Docker Networks
* Docker DNS
* Service Discovery
* Container Communication
* Database Initialization
* Network Inspection
* Docker System Commands
* .dockerignore

These concepts are heavily used in production Docker environments and form the foundation for Kubernetes Persistent Volumes, Services, and Networking.

---

# Conclusion

In this practical session, we successfully created a PostgreSQL database container using Docker Volumes and Docker Networks.

We demonstrated how data can be stored persistently using Docker Volumes and how containers can communicate using Docker Networks without requiring manual IP configuration.

These concepts are critical for designing scalable, reliable, and production-ready containerized applications.
