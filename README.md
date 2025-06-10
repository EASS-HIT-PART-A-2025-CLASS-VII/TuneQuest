🎶 TuneQuest
A full-stack music discovery app that helps you explore music, get AI-powered recommendations, and save your favorite tracks, albums, and artists.

✨ Features
🔍 Browse music (tracks, albums, artists)

❤️ Save favorites to your personal list

🤖 Get personalized AI recommendations (via Google Generative AI)

💬 Upcoming: Chat with an AI music companion

🚀 Tech Stack
Backend
FastAPI – High-performance Python web framework

PostgreSQL (via asyncpg) – Asynchronous relational database

SQLAlchemy (async) – ORM for Python

Alembic – Schema migrations

Google Generative AI API – Smart music recommendations

Frontend
React (Vite) – Lightning-fast UI framework

TypeScript – Type-safe development

React Router – Client-side routing

📁 Project Structure
php
Copy
Edit
TuneQuest/
├── backend/              # Backend application
│   ├── app/              # FastAPI app
│   │   ├── api/          # Route handlers
│   │   ├── core/         # DB config, settings
│   │   ├── crud/         # DB access logic
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── main.py       # FastAPI entrypoint
│   ├── tests/            # Unit and integration tests
│   └── migrations/       # Alembic migrations
├── frontend/             # Frontend application
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable UI components
│   │   └── contexts/     # React context providers
│   └── public/           # Static assets
└── docker/               # Docker configuration (optional)
🛠️ Development Setup
Prerequisites
Node.js 18+

Python 3.11+

PostgreSQL 15+

(Optional) Docker & Docker Compose

1. Clone the repository
bash
Copy
Edit
git clone https://github.com/your-username/tunequest.git
cd tunequest
2. Set up the backend
bash
Copy
Edit
cd backend
pip install -r requirements.txt
If you're not using a virtual environment, make sure dependencies don't conflict globally.

3. Set up the frontend
bash
Copy
Edit
cd ../frontend
npm install
4. Start development servers
Without Docker:

bash
Copy
Edit
# In one terminal
cd backend
uvicorn app.main:app --reload

# In another terminal
cd frontend
npm run dev
With Docker (optional):

bash
Copy
Edit
docker-compose up --build
🔗 URLs
Frontend: http://localhost:5173

Backend API: http://localhost:8000

PostgreSQL: localhost:5432

📝 Environment Variables
(Optional) Create .env files in the backend and frontend directories:

backend/.env

ini
Copy
Edit
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=tunequest_db
DB_URL=postgresql://your_db_user:your_db_password@localhost:5432/tunequest_db
BACKEND_PORT=8000
frontend/.env

ini
Copy
Edit
VITE_API_URL=http://localhost:8000
🧪 Testing
Testing is powered by pytest and httpx.

Backend unit tests are located in backend/tests/

Integration tests cover key API routes (favorites, auth, etc.)

To run tests:

bash
Copy
Edit
cd backend
pytest
📦 Deployment
Coming soon: Docker Compose + production server setup with full deployment instructions.