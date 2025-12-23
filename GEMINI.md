# SupplyGuard AI (GEMINI Context)

## 🚀 Project Overview
**SupplyGuard AI** is an AI-powered supply chain risk intelligence system developed for the **One AI Hackathon 2025**. It is designed to predict supply chain disruptions 30-60 days in advance and recommend mitigation strategies.

**Core Goal:** Move from reactive planning to predictive decision intelligence for the "ABC Integrated Supply Chain" (or similar scenarios like KFC Pakistan as noted in code).

**Key Features:**
*   **Predictive Risk Scoring:** Analyze vulnerabilities in suppliers and logistics.
*   **Early Warning System:** Predict disruptions (delays, stock shortages).
*   **Mitigation Engine:** AI-driven recommendations (diversification, rerouting).
*   **AI Agent:** Conversational interface for supply chain insights (powered by OpenAI).

## 🛠️ Tech Stack

### Frontend
*   **Framework:** Next.js 16.1.0 (App Router)
*   **Language:** TypeScript
*   **Styling:** Tailwind CSS v4, Radix UI, Lucide React
*   **State:** React 19.2.3

### Backend
*   **Framework:** FastAPI
*   **Language:** Python 3.13+
*   **Dependency Manager:** `uv` (project uses `pyproject.toml` with `hatchling`)
*   **Database:** PostgreSQL (Neon DB), accessed via `SQLModel` / `asyncpg`
*   **AI/ML:** OpenAI API (`openai-agents` SDK)

## 🏗️ Building and Running

### Prerequisites
*   Node.js & npm
*   Python 3.13+
*   `uv` (Python package manager)
*   PostgreSQL database (Neon)
*   OpenAI API Key

### Backend Setup (`backend/`)
1.  **Navigate to directory:**
    ```bash
    cd backend
    ```
2.  **Install dependencies:**
    ```bash
    uv sync
    ```
3.  **Environment Variables:**
    Create a `.env` file in `backend/` with:
    ```env
    OPENAI_API_KEY=sk-...
    DATABASE_URL=postgresql://user:pass@host/db
    ```
4.  **Run Development Server:**
    ```bash
    uv run dev
    # OR directly
    uv run python -m uvicorn backend.main:app --reload
    ```
    *API Docs available at:* `http://localhost:8000/docs`

### Frontend Setup (`frontend/`)
1.  **Navigate to directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run Development Server:**
    ```bash
    npm run dev
    ```
    *App available at:* `http://localhost:3000`

## 📂 Key Directories

### `backend/src/backend/`
*   `main.py`: Application entry point, FastAPI app setup, CORS, and router inclusion.
*   `config.py`: Configuration management using `pydantic-settings`.
*   `database.py`: Database connection and session management (SQLModel).
*   `agent/`: AI Agent logic (Tools, Prompts, Client).
*   `api/routes/`: API endpoints organized by domain (risks, suppliers, chat, etc.).
*   `models/`: Pydantic/SQLModel schemas.
*   `services/`: Business logic (Risk scoring, Simulation, Analysis).

### `frontend/app/`
*   `(dashboard)/`: Main application layout and pages.
*   `components/`: Reusable UI components (Charts, Chat interface, Tables).
*   `lib/api.ts`: API integration utilities.

## 📝 Development Conventions
*   **Code Style:** Follow Python PEP 8 (implied) and Standard JS/TS conventions (ESLint configured).
*   **Backend Imports:** Absolute imports used (e.g., `from backend.config import ...`).
*   **Database:** Uses `SQLModel` for ORM. Ensure schema changes are reflected in models.
*   **AI Integration:** Centralized in `backend/agent/` and exposed via `api/routes/chat.py`.

## ⚠️ Notes for Hackathon
*   **Focus:** Functionality over perfect test coverage.
*   **Data:** Likely uses synthetic or generated data (`scripts/populate_db.py` exists).
*   **AI Model:** Defaults to `gpt-4o`.
