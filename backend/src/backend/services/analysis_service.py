from typing import Dict, Any

# Simple heuristics/AI wrapper for generating entity-specific insights
# In a real scenario, this would call the LLM with a specific Prompt Template for "Summarization"

async def generate_supplier_analysis(supplier_data: Dict) -> Dict[str, Any]:
    """
    Generates a structured analysis for a supplier.
    """
    risk_score = supplier_data.get("risk_score", 0)
    
    # Heuristic-based analysis fallback (mimicking AI)
    if risk_score > 70:
        summary = "CRITICAL RISK: High dependency concentration and recent quality alerts."
        recommendation = "Immediate diversification required."
    elif risk_score > 50:
        summary = "MODERATE RISK: Monitoring required due to regional delays."
        recommendation = "Review backup suppliers."
    else:
        summary = "LOW RISK: Supplier performing within optimal parameters."
        recommendation = "Maintain current volume."
        
    return {
        "summary": summary,
        "recommendation": recommendation,
        "risk_breakdown": {
            "reliability": "High" if risk_score < 30 else "Low", 
            "financial": "Stable"
        }
    }

async def generate_outlet_analysis(outlet_data: Dict) -> Dict[str, Any]:
    days = outlet_data.get("chicken_days_remaining", 5)
    
    if days < 2:
        return {"alert": "CRITICAL INVENTORY", "action": "Expedite delivery immediately."}
    return {"status": "Healthy stock levels"}
