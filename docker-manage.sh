#!/bin/bash
# Script to manage Docker containers for Nash Equilibrium Finder

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Variables
PROD_COMPOSE="docker-compose.yml"
DEV_COMPOSE="docker-compose.dev.yml"

# Function to display usage help
show_help() {
    echo -e "Usage: $0 [option] [mode]"
    echo -e "Options:"
    echo -e "  start    Start containers"
    echo -e "  stop     Stop containers"
    echo -e "  restart  Restart containers"
    echo -e "  logs     View container logs"
    echo -e "  build    Rebuild containers"
    echo -e "  clean    Remove all containers and images"
    echo -e "Modes:"
    echo -e "  dev      Development mode (default)"
    echo -e "  prod     Production mode"
}

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker and Docker Compose are required but not installed${NC}"
    exit 1
fi

# Check arguments
if [ $# -lt 1 ]; then
    show_help
    exit 1
fi

# Determine which compose file to use
MODE=$2
if [ "$MODE" = "prod" ]; then
    COMPOSE_FILE=$PROD_COMPOSE
    MODE_TEXT="production"
else
    COMPOSE_FILE=$DEV_COMPOSE
    MODE_TEXT="development"
    MODE="dev"
fi

case $1 in
    start)
        echo -e "${GREEN}Starting Nash Equilibrium Finder in $MODE_TEXT mode...${NC}"
        docker-compose -f $COMPOSE_FILE up -d
        echo -e "${GREEN}Services started:${NC}"
        if [ "$MODE" = "dev" ]; then
            echo -e "${YELLOW}Frontend:${NC} http://localhost:3000"
            echo -e "${YELLOW}Backend:${NC} http://localhost:5000"
            echo -e "${YELLOW}Waiting for services to be ready...${NC}"
            sleep 10
            echo -e "${GREEN}Services should be available now${NC}"
        else
            echo -e "${YELLOW}Frontend:${NC} http://localhost:80"
            echo -e "${YELLOW}Backend API:${NC} http://localhost:5000"
            echo -e "${YELLOW}Waiting for services to be ready...${NC}"
            sleep 15
            echo -e "${GREEN}Services should be available now${NC}"
        fi
        ;;
        
    stop)
        echo -e "${YELLOW}Stopping Nash Equilibrium Finder in $MODE_TEXT mode...${NC}"
        docker-compose -f $COMPOSE_FILE down
        echo -e "${GREEN}Services stopped${NC}"
        ;;
        
    restart)
        echo -e "${YELLOW}Restarting Nash Equilibrium Finder in $MODE_TEXT mode...${NC}"
        docker-compose -f $COMPOSE_FILE down
        docker-compose -f $COMPOSE_FILE up -d
        echo -e "${GREEN}Services restarted${NC}"
        ;;
        
    logs)
        echo -e "${YELLOW}Viewing logs for Nash Equilibrium Finder in $MODE_TEXT mode...${NC}"
        docker-compose -f $COMPOSE_FILE logs -f
        ;;
        
    build)
        echo -e "${YELLOW}Rebuilding Nash Equilibrium Finder in $MODE_TEXT mode...${NC}"
        docker-compose -f $COMPOSE_FILE build --no-cache
        echo -e "${GREEN}Services rebuilt${NC}"
        ;;
        
    clean)
        echo -e "${RED}Removing all Nash Equilibrium Finder containers and images...${NC}"
        docker-compose -f $PROD_COMPOSE down --rmi all --volumes --remove-orphans
        docker-compose -f $DEV_COMPOSE down --rmi all --volumes --remove-orphans
        echo -e "${GREEN}Cleanup complete${NC}"
        ;;
        
    *)
        show_help
        exit 1
        ;;
esac

exit 0
