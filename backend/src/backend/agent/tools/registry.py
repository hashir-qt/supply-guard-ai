from typing import List, Callable, Dict
from backend.agent.tools.overview_tools import get_supply_chain_overview
from backend.agent.tools.supplier_tools import analyze_supplier_risk
from backend.agent.tools.outlet_tools import check_outlet_status
from backend.agent.tools.simulation_tools import simulate_disruption

# Define tool definitions for OpenAI function calling
TOOLS_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_supply_chain_overview",
            "description": "Get an overview of the current supply chain health, including risk scores and alerts.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_supplier_risk",
            "description": "Analyze the risk profile and status of a specific supplier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "supplier_id": {"type": "string", "description": "The ID of the supplier (e.g., SUP-001)"}
                },
                "required": ["supplier_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_outlet_status",
            "description": "Check the inventory and operational status of a specific outlet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "outlet_id": {"type": "string", "description": "The ID of the outlet (e.g., KHI-001)"}
                },
                "required": ["outlet_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "simulate_disruption",
            "description": "Simulate a hypothetical disruption to see its cascading relationships and impact.",
            "parameters": {
                "type": "object",
                "properties": {
                    "disruption_type": {"type": "string", "enum": ["supplier_failure", "demand_surge", "logistics_delay"]},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                    "duration_days": {"type": "integer"}
                },
                "required": ["disruption_type", "severity", "duration_days"],
            },
        },
    }
]

# Map names to actual python functions
AVAILABLE_TOOLS: Dict[str, Callable] = {
    "get_supply_chain_overview": get_supply_chain_overview,
    "analyze_supplier_risk": analyze_supplier_risk,
    "check_outlet_status": check_outlet_status,
    "simulate_disruption": simulate_disruption
}
