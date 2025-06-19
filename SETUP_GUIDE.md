# TuneQuest Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Docker Desktop**
   - Download and install from: https://www.docker.com/products/docker-desktop
   - Make sure Docker Desktop is running

2. **Git** (if cloning the repository)
   - Download and install from: https://git-scm.com/downloads

3. **Python 3.12** (for backend development)
   - Download and install from: https://www.python.org/downloads/

4. **Node.js** (for frontend development)
   - Download and install from: https://nodejs.org/

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd TuneQuest

2. Create a .env file in the root directory with the following content:
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432
DB_NAME=TuneQuest
JWT_SECRET_KEY=your-jwt-secret-key
DB_URL=postgresql+asyncpg://postgres:your-db-password@db:5432/TuneQuest
MIGRATION_DB_URL=postgresql+psycopg2://postgres:your-db-password@db:5432/TuneQuest
BACKEND_PORT=8000
MUSIC_SERVICE_PORT=8001
API_BASE_URL=http://localhost:8000
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
GOOGLE_API_KEY=your-google-api-key
ENV=development

3. create .env.test in the backend and music-service directories with the following content:

backend:
TEST_DB_URL=postgresql+asyncpg://postgres:your-db-password@db:5432/TuneQuest_backend_test
ENV=testing
GEMINI_API_KEY=your-gemini-api-key
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret

music-service:
TEST_DB_URL=postgresql+asyncpg://postgres:your-db-password@db:5432/TuneQuest_music_service_test
ENV=testing
GEMINI_API_KEY=your-gemini-api-key
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret

4. Build and start the services:
```bash
# First build the containers
docker compose build --no-cache

# Then start the services
docker compose up

5. Set up the database:
# First, stop any existing containers
docker compose down

# Then start only the database
docker compose up -d db

# Set up the database
.\setup-database.ps1

6. Start all services:
docker compose up