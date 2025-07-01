# Docker Setup for Nash Equilibrium Finder

This document explains how to use Docker with the Nash Equilibrium Finder project.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

The project includes a management script to simplify Docker operations:

```bash
# Start in development mode
./docker-manage.sh start dev

# Start in production mode
./docker-manage.sh start prod
```

## Project Structure

- `Dockerfile`: Configuration for the Python backend
- `Dockerfile.frontend`: Configuration for the React frontend
- `docker-compose.yml`: Production configuration
- `docker-compose.dev.yml`: Development configuration
- `docker-manage.sh`: Management script

## Development Mode

Development mode provides hot-reloading for both the frontend and backend:

```bash
./docker-manage.sh start dev
```

This will:
- Start the Flask backend with auto-reload at http://localhost:5000
- Start the React development server at http://localhost:3000
- Mount source code as volumes for real-time changes

## Production Mode

Production mode optimizes the application for deployment:

```bash
./docker-manage.sh start prod
```

This will:
- Build an optimized React production build
- Serve static files via Nginx
- Serve the API via Gunicorn
- Make the application available at http://localhost

## Docker Management Script

The `docker-manage.sh` script provides several commands:

```bash
# Usage
./docker-manage.sh [command] [mode]

# Commands
start    # Start containers
stop     # Stop containers
restart  # Restart containers
logs     # View container logs
build    # Rebuild containers
clean    # Remove all containers and images

# Modes
dev      # Development mode
prod     # Production mode
```

## Manual Docker Commands

If you prefer to use Docker commands directly:

### Development

```bash
# Start development containers
docker-compose -f docker-compose.dev.yml up

# Rebuild and start
docker-compose -f docker-compose.dev.yml up --build
```

### Production

```bash
# Start production containers
docker-compose up -d

# Rebuild and start
docker-compose up --build -d
```

## Troubleshooting

If you encounter issues:

1. Check container status:
   ```bash
   docker ps -a
   ```

2. Check logs:
   ```bash
   ./docker-manage.sh logs dev
   # or
   ./docker-manage.sh logs prod
   ```

3. Clean and rebuild:
   ```bash
   ./docker-manage.sh clean
   ./docker-manage.sh build dev
   ./docker-manage.sh start dev
   ```
