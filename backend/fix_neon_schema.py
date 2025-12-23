#!/usr/bin/env python3
"""
CRITICAL: Drop and recreate Neon DB with NEW schema (no hardcoded risk scores)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 70)
print("FIXING NEON DATABASE - Removing hardcoded risk_score fields")
print("=" * 70)

# Force reload config
import importlib
from backend import config as config_module
importlib.reload(config_module)

from sqlmodel import SQLModel, Session
from backend.database import engine
from backend.data.generator import (
    generate_suppliers, generate_outlets, generate_routes,
    generate_risks, generate_events, generate_history
)
from backend.models import schemas

print("\n1. Dropping ALL tables from Neon DB...")
try:
    SQLModel.metadata.drop_all(engine)
    print("✓ Old tables dropped (with hardcoded risk_score fields)")
except Exception as e:
    print(f"⚠ Warning during drop: {e}")

print("\n2. Creating NEW tables (dynamic schema - NO risk_score fields)...")
try:
    SQLModel.metadata.create_all(engine)
    print("✓ New tables created")
    print("   - Supplier table: NO risk_score field")
    print("   - Outlet table: NO current_risk_score field")
    print("   - Risk scores will be calculated on-the-fly!")
except Exception as e:
    print(f"❌ Error creating tables: {e}")
    sys.exit(1)

print("\n3. Populating with CLEAN data (base metrics only)...")
try:
    with Session(engine) as session:
        suppliers = generate_suppliers()
        print(f"  - Adding {len(suppliers)} suppliers")
        session.add_all(suppliers)
        
        outlets = generate_outlets()
        print(f"  - Adding {len(outlets)} outlets")
        session.add_all(outlets)
        
        routes = generate_routes()
        print(f"  - Adding {len(routes)} delivery routes")
        session.add_all(routes)
        
        risks = generate_risks()
        print(f"  - Adding {len(risks)} initial risks")
        session.add_all(risks)
        
        events = generate_events()
        print(f"  - Adding {len(events)} calendar events") 
        session.add_all(events)
        
        history = generate_history()
        print(f"  - Adding {len(history)} historical incidents")
        session.add_all(history)
        
        session.commit()
        print("✓ All data committed to Neon DB")
except Exception as e:
    print(f"❌ Error populating data: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("SUCCESS! Neon DB is now DYNAMIC")
print("=" * 70)
print("\n✅ Suppliers store: reliability %, quality %, metrics")
print("✅ Outlets store: inventory levels, chicken_days_remaining")
print("✅ Risk scores: CALCULATED ON-THE-FLY from metrics")
print("\n🚀 Start server: uvicorn backend.main:app --port 8001")
print("📊 Test: GET /api/suppliers/ (will compute risk scores dynamically)")
