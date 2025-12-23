# SupplyGuard AI Backend API

## 🧠 Overview

The SupplyGuard AI backend is a Python-based API server that powers the AI-driven supply chain disruption prediction system. It handles data processing, machine learning model inference, risk scoring algorithms, and provides RESTful endpoints for the frontend application.

## 🛠️ Tech Stack

- **Language**: Python 3.13+
- **Package Manager**: uv (recommended) or pip
- **Framework**: [FastAPI/TensorFlow/PyTorch - to be implemented]
- **AI/ML Libraries**: [To be determined based on model requirements]
- **Database**: [To be implemented - PostgreSQL/MongoDB/Elasticsearch]

## 📁 Project Structure

```
backend/
├── README.md              # This file
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock               # Dependency lock file
├── .python-version       # Python version specification
├── .venv/                # Virtual environment (gitignored)
└── src/
    └── backend/          # Source code package
        └── __init__.py
```

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- uv package manager (recommended) or pip

### Installation

1. **Create virtual environment and install dependencies:**
   ```bash
   cd backend
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

2. **Alternative with pip:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

### Running the Server

During development:
```bash
# Activate virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the development server
python -m backend
```

## 🏗️ API Endpoints

*Documentation will be updated as endpoints are implemented*

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check endpoint |
| `/api/predict` | POST | Supply chain disruption prediction |
| `/api/risk-score` | POST | Calculate risk score for supply chain |
| `/api/mitigation` | POST | Get mitigation recommendations |

## 🤖 AI/ML Components

The backend will include:
- Machine learning models for disruption prediction
- Risk scoring algorithms
- Data preprocessing pipelines
- Feature engineering components
- Model evaluation and validation systems

## 🔧 Configuration

Environment variables (to be implemented):
- `DATABASE_URL`: Database connection string
- `MODEL_PATH`: Path to trained ML models
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARN, ERROR)
- `API_KEY`: Authentication key for API access

## 🧪 Testing

Testing framework and instructions will be added during development:
```bash
# Run tests (TBD)
# uv run pytest
```

## 📈 Deployment

Deployment configurations will be added during development:
- Docker containerization
- Environment-specific configurations
- CI/CD pipeline setup

## 📄 License

[License information to be determined by the team]

---

Part of the SupplyGuard AI project for One AI Hackathon 2025