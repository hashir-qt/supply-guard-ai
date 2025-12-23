"""
AI Agent API Endpoint
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

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with SupplyGuard AI Agent.
    
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

@router.post("/chat/stream")
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

@router.get("/capabilities")
async def get_capabilities():
    """
    Get agent capabilities and example queries.
    """
    return {
        "agent": "SupplyGuard AI Analyst",
        "model": "gpt-4o",
        "capabilities": [
            {
                "name": "Supply Chain Overview",
                "tool": "get_supply_chain_overview",
                "examples": ["How's our supply chain?", "Overall status?", "Give me an overview"]
            },
            {
                "name": "Supplier Analysis",
                "tool": "analyze_supplier_risk",
                "examples": ["Risk with K&N's?", "Analyze Malik Farms", "Which suppliers are risky?"]
            },
            {
                "name": "Outlet Status",
                "tool": "check_outlet_status",
                "examples": ["How's KFC Clifton?", "Karachi outlets status?", "Low inventory outlets?"]
            },
            {
                "name": "Demand Forecasting",
                "tool": "forecast_demand",
                "examples": ["PSL final demand?", "Ramadan forecast?", "Next week demand?"]
            },
            {
                "name": "External Risks",
                "tool": "check_external_risks",
                "examples": ["Upcoming events?", "External risks?", "When's Ramadan?"]
            },
            {
                "name": "Disruption Simulation",
                "tool": "simulate_disruption",
                "examples": ["What if K&N's fails?", "Simulate monsoon", "Model supplier shutdown"]
            },
            {
                "name": "Recommendations",
                "tool": "get_recommendations",
                "examples": ["What should we do?", "Give me recommendations", "Top actions?"]
            }
        ],
        "suggested_queries": [
            "What are our top risks right now?",
            "How's our chicken supply looking?",
            "Prepare me for PSL final",
            "What if we lose K&N's for a week?",
            "Which outlets need urgent attention?",
            "Give me recommendations for today"
        ]
    }
