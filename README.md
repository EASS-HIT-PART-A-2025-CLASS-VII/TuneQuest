# 🎶 TuneQuest

> A full-stack music discovery app that helps you explore music, get AI-powered recommendations, and save your favorite tracks, albums, and artists.

## ✨ Features

- 🔍 Browse music (tracks, albums, artists)
- ❤️ Save favorites to your personal list
- 🤖 Get personalized AI recommendations (via Google Generative AI)
- 💬 Upcoming: Chat with an AI music companion

## 🚀 Tech Stack

### Backend
- **FastAPI** – High-performance Python web framework
- **PostgreSQL** (via asyncpg) – Asynchronous relational database
- **SQLAlchemy** (async) – ORM for Python
- **Alembic** – Schema migrations
- **Google Generative AI API** – Smart music recommendations

### Frontend
- **React** (Vite) – Lightning-fast UI framework
- **TypeScript** – Type-safe development
- **React Router** – Client-side routing

![Homepage Screenshot](frontend/src/assets/home-page.png)
![Companion Page Screenshot](frontend/src/assets/companion-page.png)
![Album Screenshot](frontend/src/assets/silk-sonic.png)

## 📁 Project Structure

```
TuneQuest/
├── backend/              # Backend application
│   ├── app/             # FastAPI app
│   │   ├── api/         # Route handlers
│   │   ├── core/        # DB config, settings
│   │   ├── crud/        # DB access logic
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── main.py      # FastAPI entrypoint
│   ├── tests/           # Unit and integration tests
│   └── migrations/      # Alembic migrations
├── frontend/            # Frontend application
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── components/  # Reusable UI components
│   │   └── contexts/    # React context providers
│   └── public/          # Static assets
└── docker/             # Docker configuration (optional)
```

## 🛠️ Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- (Optional) Docker & Docker Compose

### Installation

1. Clone the repository
```bash
git clone https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/TuneQuest.git
cd tunequest
```

2. Set up the backend
```bash
cd backend
pip install -r requirements.txt
```

> If you're not using a virtual environment, make sure dependencies don't conflict globally.

3. Set up the frontend
```bash
cd ../frontend
npm install
```

### Running the Application

#### Without Docker

Run both services in separate terminals:

```bash
# Backend (in one terminal)
cd backend
uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
npm run dev
```

#### With Docker (Optional)

```bash
docker-compose up --build
```

## 🔗 URLs

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432

## 📝 Environment Variables

Create `.env` files in the `backend/` and `frontend/` directories.

You can copy and rename `.env.example` to `.env` to get started.

### 🔧 `.env` (for development)
```ini
# Database settings
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=tunequest_db
DB_HOST=localhost               # or 'db' if using Docker
DB_PORT=5432
DB_URL=postgresql+asyncpg://your_db_user:your_db_password@localhost:5432/tunequest_db

# Optional: Used only for Alembic migrations (uses psycopg2)
MIGRATION_DB_URL=postgresql+psycopg2://your_db_user:your_db_password@db:5432/tunequest_db

# Backend config
BACKEND_PORT=8000
ENV=development                 # Options: development, testing

# Auth
JWT_SECRET_KEY=your_jwt_secret_key

# External APIs
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
GOOGLE_API_KEY=your_google_api_key

# 🧪 .env.test (for running tests)

# Async test database connection (used by SQLAlchemy + AsyncSession)
TEST_DB_URL=postgresql+asyncpg://your_db_user:your_db_password@localhost:5432/tunequest_test

# External API keys (can be mocked or reused from dev)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
GOOGLE_API_KEY=your_google_api_key

# App environment
ENV=testing

## 🧪 Testing

Testing is powered by pytest and httpx.

Backend unit tests are located in `backend/tests/`
Integration tests cover key API routes (favorites, auth, etc.)

```bash
cd backend
pytest
```

## 📦 Deployment

Coming soon: Docker Compose + production server setup with full deployment instructions.

---

> Made with ❤️ by Dvir Manos | [GitHub](https://github.com/zoroflamingo/tunequest)