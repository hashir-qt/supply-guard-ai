"""
AI Agent Chat Endpoint - Using OpenAI Agents SDK (NOT raw completions API)
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    tools_used: List[str]
    conversation_id: str

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with SupplyGuard AI Agent using OpenAI Agents SDK.
    
    The agent uses real-time data from the database to answer supply chain questions.
    """
    from backend.agent.supply_chain_agent import run_agent
    
    try:
        response, tools_used = await run_agent(request.message)
        
        return ChatResponse(
            response=response,
            tools_used=tools_used,
            conversation_id=request.conversation_id or "new"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream chat responses for real-time UX.
    Returns Server-Sent Events.
    """
    from backend.agent.supply_chain_agent import run_agent_stream
    
    async def generate():
        try:
            async for event in run_agent_stream(request.message):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/status")
async def get_agent_status():
    """Check if AI agent is configured and ready"""
    from backend.config import get_settings
    settings = get_settings()
    
    return {
        "agent_ready": bool(settings.OPENAI_API_KEY),
        "model": "gpt-4o",
        "tools_count": 11,
        "available_tools": [
            "get_supply_chain_overview",
            "analyze_supplier_risk",
            "get_at_risk_suppliers",
            "check_outlet_status",
            "get_low_inventory_outlets",
            "simulate_disruption",
            "get_simulation_scenarios",
            "forecast_demand",
            "check_external_risks",
            "get_recommendations",
            "get_historical_incidents"
        ]
    }

@router.get("/capabilities")
async def get_capabilities():
    """Get agent capabilities and example queries"""
    return {
        "agent": "SupplyGuard AI Analyst",
        "model": "gpt-4o",
        "capabilities": [
            {"name": "Supply Chain Overview", "examples": ["How's our supply chain?", "Give me an overview"]},
            {"name": "Supplier Analysis", "examples": ["Risk with K&N's?", "Analyze Malik Farms"]},
            {"name": "Outlet Status", "examples": ["How's KFC Clifton?", "Low inventory outlets?"]},
            {"name": "Demand Forecasting", "examples": ["PSL final demand?", "Ramadan forecast?"]},
            {"name": "External Risks", "examples": ["Upcoming events?", "When's Ramadan?"]},
            {"name": "Disruption Simulation", "examples": ["What if K&N's fails?", "Simulate monsoon"]},
            {"name": "Recommendations", "examples": ["What should we do?", "Top actions?"]}
        ],
        "suggested_queries": [
            "What are our top risks right now?",
            "How's our chicken supply looking?",
            "Prepare me for PSL final",
            "What if we lose K&N's for a week?",
            "Which outlets need urgent attention?"
        ]
    }
