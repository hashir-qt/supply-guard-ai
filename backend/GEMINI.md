# SupplyGuard AI (Backend Context)

## 🚀 Project Overview

**SupplyGuard AI** is an AI-powered supply chain risk intelligence system designed to predict disruptions and recommend mitigation strategies. It acts as a predictive decision intelligence tool, specifically modeled for complex supply chains like **KFC Pakistan** (poultry farms, processing, logistics to outlets).

**Core Goal:** Move from reactive planning to predictive risk management by forecasting disruptions 30-60 days in advance.

### 🔑 Key Features
*   **Predictive Risk Scoring:** Real-time risk assessment for suppliers, logistics routes, and demand spikes.
*   **AI Analyst Agent:** A conversational interface powered by OpenAI's `openai-agents` SDK that can analyze data, run simulations, and answer supply chain queries.
*   **Simulation Engine:** "What-if" scenario planning for disruptions (e.g., fuel strikes, disease outbreaks).
*   **Integration:** Connects various data points: Suppliers (Tier 1-3), Outlets (Zones: Karachi, Lahore, etc.), and Events (Religious, Political).

## 🛠️ Tech Stack & Architecture

### Backend Core
*   **Framework:** FastAPI
*   **Language:** Python 3.13+
*   **Dependency Manager:** `uv` (recommended)
*   **Entry Point:** `src/backend/main.py`

### Data & Storage
*   **Database:** PostgreSQL (Neon DB)
*   **ORM:** SQLModel (SQLAlchemy + Pydantic)
*   **Migration/Schema:** Defined in `src/backend/models/schemas.py`

### AI & Intelligence
*   **LLM:** OpenAI (GPT-4o)
*   **Agent Framework:** `openai-agents` SDK
*   **Agent Logic:** `src/backend/agent/supply_chain_agent.py`

## 📂 Directory Structure

```
backend/
├── pyproject.toml         # Dependencies and build config
├── .env                   # Environment variables (OPENAI_API_KEY, DATABASE_URL)
└── src/
    └── backend/
        ├── main.py        # Application entry point
        ├── config.py      # Configuration management
        ├── database.py    # DB connection and session handling
        ├── agent/         # AI Agent logic and tool definitions
        │   ├── supply_chain_agent.py # Main agent definition
        │   └── tools/     # Tools available to the agent (simulation, forecast, etc.)
        ├── api/           # REST API Routes
        │   └── routes/    # Endpoints (risks, suppliers, chat, etc.)
        ├── models/        # SQLModel schemas
        │   └── schemas.py # Core data models (Supplier, Outlet, Risk, etc.)
        └── services/      # Business logic (Risk calculation, Analysis)
```

## 🏗️ Development Workflow

### Prerequisites
*   Python 3.13+
*   `uv` (https://github.com/astral-sh/uv)
*   PostgreSQL database (or valid connection string)

### Setup
1.  **Install Dependencies:**
    ```bash
    uv sync
    ```
2.  **Environment Configuration:**
    Create a `.env` file in `backend/` containing:
    ```env
    OPENAI_API_KEY=sk-...
    DATABASE_URL=postgresql://user:pass@host/db
    DEBUG=True
    ```
3.  **Run Development Server:**
    ```bash
    uv run dev
    # OR
    uv run python -m uvicorn backend.main:app --reload
    ```
    API documentation is available at `http://localhost:8000/docs`.

### Database Management
*   **Initialization:** The `init_db()` function in `database.py` creates tables based on models.
*   **Population:** Scripts like `scripts/populate_db.py` (if available) are used to seed data.

## 📝 Code Conventions

*   **Imports:** Use absolute imports starting with `backend.` (e.g., `from backend.models.schemas import Supplier`).
*   **Typing:** Strong typing with Pydantic and SQLModel is enforced.
*   **Async:** FastAPI routes should be `async def`.
*   **Agent Tools:** Agent tools are defined in `src/backend/agent/tools/` and must be registered in the agent definition.

## 🧠 Domain Context (KFC Pakistan)

The data models reflect a specific supply chain structure:
*   **Suppliers:** Chicken Processors, Poultry Farms, Fresh Produce, Packaging, etc.
*   **Zones:** Major Pakistani cities (Karachi, Lahore, Islamabad, etc.).
*   **Events:** Specific local event types (Religious, Political, Weather) that impact demand/logistics.
*   **Risks:** Categorized by Supplier, Logistics, Demand, and External factors.
