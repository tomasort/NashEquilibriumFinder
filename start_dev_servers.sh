#!/bin/bash
# Script to start both the frontend and backend servers

# Check if Python and npm are installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed"
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to handle script termination
cleanup() {
    echo -e "\n${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up trap to catch termination signal
trap cleanup INT TERM

# Start the backend server
echo -e "${GREEN}Starting Flask backend server...${NC}"
cd "$(dirname "$0")"
python3 web_api.py &
BACKEND_PID=$!

# Wait a bit for the backend to start
sleep 2

# Start the frontend development server
echo -e "${GREEN}Starting React frontend server...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!

# Wait for processes to finish
echo -e "${GREEN}Both servers are running. Press Ctrl+C to stop both.${NC}"
echo -e "${YELLOW}Backend:${NC} http://localhost:5000"
echo -e "${YELLOW}Frontend:${NC} http://localhost:3000"
wait $BACKEND_PID $FRONTEND_PID
