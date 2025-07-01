# Nash Equilibrium Finder Frontend

This is the frontend application for the Nash Equilibrium Finder project.

## Overview

This React-based UI provides a user-friendly interface for:
- Creating and analyzing game theory games
- Finding Nash equilibria (pure and mixed strategies)
- Experimenting with mixed strategies
- Visualizing payoffs and equilibria

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm (version 6 or higher)

### Installation

1. Install frontend dependencies:

```bash
cd frontend
npm install
```

2. Start the frontend development server:

```bash
npm start
```

The frontend application will be available at [http://localhost:3000](http://localhost:3000).

### Backend Integration

The frontend is configured to work with the Flask API running at http://localhost:5000.

To start the backend server:

```bash
# Install backend dependencies (from project root)
pip install -r requirements.txt

# Start the Flask API
python web_api.py
```

## Project Structure

- `/src/components`: Reusable UI components
- `/src/pages`: Main application pages
- `/src/services`: API integration services
- `/src/context`: React context for state management
- `/src/utils`: Utility functions and helpers

## Features

- Interactive payoff matrix visualization
- Game creation from templates or custom definitions
- Nash equilibrium analysis
- Mixed strategy testing with adjustable probabilities
- Real-time expected payoff calculations

## Building for Production

To create a production build:

```bash
npm run build
```

This will create a `build` folder with optimized static files that can be served by any static file server or integrated with the Flask backend.
