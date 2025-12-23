from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings

# Import all route modules
from backend.api.routes import overview, risks, suppliers, outlets, routes, simulation, forecast, events, chat, monitor

# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 SupplyGuard AI Backend Starting...")
    
    # Ensure OpenAI API Key is in environment for SDKs
    import os
    settings = get_settings()
    if settings.OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
        print(f"✅ OpenAI API Key loaded (starts with {settings.OPENAI_API_KEY[:7]}...)")
    else:
        print("⚠️  WARNING: OpenAI API Key NOT set!")
        
    yield
    print("👋 SupplyGuard AI Backend Shutting Down")

# --- App Setup ---
settings = get_settings()
app = FastAPI(
    title="SupplyGuard AI API",
    description="AI-Powered Supply Chain Risk Intelligence for KFC Pakistan",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SupplyGuard AI", "db_connected": True}

# --- Register All Routers ---

# Core Data APIs
app.include_router(overview.router, prefix="/api/overview", tags=["Overview"])
app.include_router(risks.router, prefix="/api/risks", tags=["Risks"])
app.include_router(suppliers.router, prefix="/api/suppliers", tags=["Suppliers"])
app.include_router(outlets.router, prefix="/api/outlets", tags=["Outlets"])
app.include_router(routes.router, prefix="/api/routes", tags=["Delivery Routes"])

# Intelligence APIs
app.include_router(simulation.router, prefix="/api/simulation", tags=["Simulation"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["Forecast"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])

# Monitoring System
app.include_router(monitor.router, prefix="/api/monitor", tags=["Monitoring System"])

# AI Agent (OpenAI Agents SDK)
app.include_router(chat.router, prefix="/api/agent", tags=["AI Agent"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)