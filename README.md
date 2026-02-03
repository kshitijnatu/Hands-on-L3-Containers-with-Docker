# Hands-on L3: Containers with Docker (Flask + Redis)

## Overview
This hands-on runs a simple Flask web app that stores a page-visit counter in Redis. The stack is orchestrated with Docker Compose:

- **web**: Flask app (Python) built from the local `Dockerfile`
- **redis**: Redis server pulled from `redis:alpine`

When you refresh the page, the counter increments and persists as long as the Redis container is running.

---

## Prerequisites
- Docker Desktop
- Docker Compose v2 (available as `docker compose`)

Verify installation:
```bash
docker --version
docker compose version
```

---

## What’s in this repo
- `app.py`: Flask app that increments a Redis key (`hits`) on each request.
- `requirements.txt`: Python dependencies (`flask`, `redis`).
- `Dockerfile`: Builds the Flask image (Python Alpine base) and runs `flask run`.
- `compose.yml`: Defines and networks the `web` and `redis` services.

---

## Execution steps

### 1) Start the application with Docker Compose
From the project directory, run:
```bash
docker compose up --build
```

Expected result:
- Compose builds the `web` image using the `Dockerfile`.
- Compose pulls `redis:alpine` for the Redis container.
- The Flask app starts and listens on container port `5000`, mapped to host port `8000`.

### 2) Access the web app
Open in a browser:
- http://localhost:8000

Or use curl:
```bash
curl http://localhost:8000
```

Refresh multiple times. You should see:
- `Hello! This page has been visited 1 times.`
- then `2`, `3`, etc.

### 3) View running containers
In another terminal:
```bash
docker compose ps
```

### 4) View logs
```bash
docker compose logs -f
```

### 5) Stop the stack
To stop containers (keeps resources around):
```bash
docker compose stop
```

To stop and remove containers and the default network:
```bash
docker compose down
```

---

## How it works (key details)
- The Flask app uses the Redis hostname `redis`:
  - In `app.py`, the client is created as `redis.Redis(host='redis', port=6379)`.
  - This works because Docker Compose creates a network where service names become DNS names.
- The hit counter is stored in Redis as the key `hits`.
- On each request to `/`, the app calls `INCR hits` via the Redis Python client.
- The `get_hit_count()` function retries Redis connection up to 5 times to handle Redis not being ready immediately at startup.

---

## What I learned in this hands-on
- **Containerizing a Python/Flask app** using a `Dockerfile`:
  - Installing Python deps from `requirements.txt`,
  - Exposing and running the Flask server inside the container.
- **Multi-container orchestration with Docker Compose**:
  - Defining multiple services (`web`, `redis`),
  - Pulling an official image (`redis:alpine`) and building a local image (`web`),
  - Understanding `depends_on` (startup ordering, not readiness).
- **Service-to-service networking in Compose**:
  - Using the Compose service name (`redis`) as the hostname from the `web` container.
- **Port mapping**:
  - Mapping host port `8000` to container port `5000` (`"8000:5000"`).
- **Basic state management**:
  - The counter persists as long as the Redis container (and its data in-memory) remains running.
  - Removing the Redis container resets the counter unless a volume is configured (not used in this hands-on).
---