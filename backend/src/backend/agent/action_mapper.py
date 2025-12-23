from typing import Dict, Any, List

def map_tool_to_action(tool_name: str, tool_args: Dict[str, Any], tool_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Translates a tool execution into a frontend UI action.
    """
    actions = []
    
    if tool_name == "analyze_supplier_risk":
        s_id = tool_args.get("supplier_id")
        actions.append({
            "type": "navigate", 
            "value": f"/suppliers/{s_id}",
            "label": f"View Details for {s_id}"
        })
        
    elif tool_name == "check_outlet_status":
        o_id = tool_args.get("outlet_id")
        actions.append({
            "type": "navigate",
            "value": f"/outlets/{o_id}",
            "label": f"View Outlet {o_id}"
        })
        
    elif tool_name == "simulate_disruption":
        actions.append({
            "type": "render_chart",
            "component": "SimulationGraph",
            "payload": tool_result
        })
        
    return actions
