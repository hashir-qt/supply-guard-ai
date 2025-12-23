"""
SupplyGuard AI Agent - Main Agent Definition using OpenAI Agents SDK
"""
from agents import Agent, Runner
from backend.config import get_settings

settings = get_settings()

from .prompts import SUPPLY_CHAIN_AGENT_INSTRUCTIONS
from .tools.overview_tools import get_supply_chain_overview
from .tools.supplier_tools import analyze_supplier_risk, get_at_risk_suppliers
from .tools.outlet_tools import check_outlet_status, get_low_inventory_outlets
from .tools.simulation_tools import simulate_disruption, get_simulation_scenarios
from .tools.demand_tools import forecast_demand, check_external_risks
from .tools.recommendation_tools import get_recommendations, get_historical_incidents

# Create the Supply Chain Agent
supply_chain_agent = Agent(
    name="SupplyGuard AI Analyst",
    instructions=SUPPLY_CHAIN_AGENT_INSTRUCTIONS,
    tools=[
        get_supply_chain_overview,
        analyze_supplier_risk,
        get_at_risk_suppliers,
        check_outlet_status,
        get_low_inventory_outlets,
        simulate_disruption,
        get_simulation_scenarios,
        forecast_demand,
        check_external_risks,
        get_recommendations,
        get_historical_incidents
    ],
    model=settings.OPENAI_MODEL
)

async def run_agent(message: str) -> tuple[str, list[str]]:
    """Run agent and return (response, tools_used)"""
    result = await Runner.run(supply_chain_agent, message)
    
    # Extract tools used from raw responses
    tools_used = []
    for item in result.raw_responses:
        if hasattr(item, 'tool_calls') and item.tool_calls:
            for tc in item.tool_calls:
                tools_used.append(tc.function.name)
    
    return result.final_output, tools_used

async def run_agent_stream(message: str):
    """Stream agent responses for real-time UX"""
    result = Runner.run_streamed(supply_chain_agent, message)
    async for event in result.stream_events():
        yield event
