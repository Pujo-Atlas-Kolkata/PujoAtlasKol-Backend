# Django Docker Project

This project is a basic Django application containerized using Docker. It is set up to run locally with Docker Compose, making it easy to get started and collaborate.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the application up and running:

### 1. Clone the Repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/Pujo-Atlas-Kolkata/PujoAtlasKol-Backend.git
cd PujoAtlasKol-Backend
```
### 2. Build and Run the Docker Containers

To build and run the application using Docker Compose, use the following command:

```bash
docker-compose up --build #but this will delete any data in database
```

If you want to run it in background

```bash
docker-compose up -d --build
```
This command will build the Docker images if they are not already built and start the Django application in a Docker container.

### 3. Access the Application

Once the containers are up and running, you can access the Django application in your web browser at:

```bash
http://localhost:8000
```

### 4. Stopping the Application
To stop the Docker containers, press Ctrl + C in the terminal where docker-compose up is running. Alternatively, you can run:

```bash
docker-compose down
```

### 5. Executing commands
If you want to have access to database run the following:
```bash
docker-compose exec my-postgres psql -U postgres -d postgres
```
If you want to migrate data then use:
```bash
docker-compose run web python manage.py migrate
```


