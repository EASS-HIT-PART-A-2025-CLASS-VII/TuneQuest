# 🎶 TuneQuest

> A full-stack music discovery app that helps you explore music, get AI-powered recommendations, and save your favorite tracks, albums, and artists.

## ✨ Features

- 🔍 Browse Music: Explore a vast library of tracks, albums, and artists.
- ❤️ Manage Favorites: Save your favorite music to a personal, persistent list.
- 🤖 AI Recommendations: Get music suggestions powered by the Google Generative AI API.
- 💬 AI Companion: Chat with an intelligent music assistant to find new tunes.

## 🚀 Tech Stack

### Backend
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Google Generative AI API**

### Frontend
- **React** (Vite)
- **TypeScript**
- **React Router**

## API Documentation

API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs

![Homepage Screenshot](https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/TuneQuest/blob/master/frontend/src/assets/home-page.png)
![Companion Page Screenshot](https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/TuneQuest/blob/master/frontend/src/assets/companion-page.png)
![Album Screenshot](https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/TuneQuest/blob/master/frontend/src/assets/silk-sonic.png)

## 📁 Project Structure

```
TuneQuest/
├── backend/            # Main FastAPI backend service
│   ├── app/            # FastAPI application code
│   │   ├── core/       # Core configurations
│   │   ├── crud/       # Database operations
│   │   ├── models/     # SQLAlchemy models
│   │   ├── routers/    # API routers
│   │   ├── schemas/    # Pydantic schemas
│   │   └── services/   # Business logic services
│   ├── tests/          # Unit and integration tests
│   └── alembic/        # Database migrations
│
├── frontend/           # React frontend application
│   ├── src/
│   │   ├── api/        # API client code
│   │   ├── components/ # Reusable React components
│   │   │   ├── auth/     # Authentication components
│   │   │   ├── common/   # Shared components
│   │   │   └── features/ # Feature-specific components
│   │   ├── pages/      # Page components
│   │   │   ├── auth/     # Authentication pages
│   │   │   ├── companion/ # AI companion pages
│   │   │   ├── home/     # Home page components
│   │   │   ├── music/    # Music-related pages
│   │   │   └── user/     # User profile pages
│   │   ├── contexts/ # React context providers
│   │   ├── types/      # TypeScript type definitions
│   │   │   ├── ai/       # AI-related types
│   │   │   ├── music/    # Music-related types
│   │   │   └── user/     # User-related types
│   │   └── utils/      # Helper utilities
│
└── music-service/      # Music service microservice
    ├── app/            # Service application code
    │   ├── core/       # Core configurations
    │   │   ├── crud/       # Database operations
    │   │   ├── models/     # Service models
    │   │   ├── routers/    # Service routers
    │   │   ├── schemas/    # Pydantic schemas
    │   │   └── services/   # Service-specific business logic
    │   └── tests/          # Service tests
    
## 🛠️ Development Setup

### Prerequisites

- **Node.js** 20+ (LTS version recommended)
- **Python** 3.12+
- **PostgreSQL** 17+
- **Git** (for cloning the repository)
- **Docker & Docker Compose**

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/TuneQuest.git](https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/TuneQuest.git)
cd tunequest
```

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

### Running the Application

1. Build and start the services:
```bash
# First build the containers
docker compose build --no-cache

# Then start the services
docker compose up

2. Set up the database:
# First, stop any existing containers
docker compose down

# Then start only the database
docker compose up -d db

# Set up the database
.\setup-database.ps1

3. Start all services:
docker compose up
```

## 🔗 URLs

- Frontend: http://localhost:5173 (from host machine)
- Backend API: http://backend:8000 (from other containers) / http://localhost:8000 (from host)
- Music Service: http://music-service:8001 (from other containers) / http://localhost:8001 (from host)
- PostgreSQL: db:5432 (from other containers) / localhost:5432 (from host)


## 🧪 Testing

### Backend Tests

- **Unit Tests**: Located in `backend/tests/`
- **Integration Tests**: Cover API routes (ai, auth, etc.)
- **Test Coverage**: Includes both backend and music service

Run tests:
```bash
# Run all backend tests
docker compose exec backend pytest

# Run specific test file
docker compose exec backend pytest tests/test_auth.py

### Music Service Tests

- **Unit Tests**: Located in `music-service/tests/`
- **Integration Tests**: Cover API routes (favorites, auth, etc.)
- **Test Coverage**: Includes both backend and music service

Run tests:
```bash
# Run all music service tests
docker compose exec music-service pytest

# Run specific test file
docker compose exec music-service pytest tests/test_auth.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

> Made with ❤️ by Dvir Manos | [GitHub](https://github.com/zoroflamingo/tunequest)