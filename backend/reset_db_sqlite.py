#!/usr/bin/env python3
"""
Reset database to SQLite and populate with clean data (no hardcoded risk scores)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlmodel import SQLModel
from backend.database import engine
from backend.data.generator import (
    generate_suppliers, generate_outlets, generate_routes,
    generate_risks, generate_events, generate_history
)
from backend.models import schemas
from sqlmodel import Session

print("=" * 60)
print("RESETTING DATABASE TO SQLITE")
print("=" * 60)

# Drop all tables
print("\n1. Dropping all existing tables...")
SQLModel.metadata.drop_all(engine)
print("✓ Tables dropped")

# Recreate tables with NEW schema (no risk_score fields)
print("\n2. Creating tables with NEW schema...")
SQLModel.metadata.create_all(engine)
print("✓ Tables created")

# Populate with clean data
print("\n3. Populating database...")
with Session(engine) as session:
    suppliers = generate_suppliers()
    print(f"  - Adding {len(suppliers)} suppliers (NO risk_score field)")
    session.add_all(suppliers)
    
    outlets = generate_outlets()
    print(f"  - Adding {len(outlets)} outlets (NO current_risk_score field)")
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
    print("✓ Data committed to SQLite")

print("\n" + "=" * 60)
print("SUCCESS! Database ready for demo")
print("=" * 60)
print("\nDatabase: supplyguard_demo.db (SQLite)")
print("Schema: Dynamic (risk scores calculated on-the-fly)")
print("\nTest with: python -c 'from backend.models.schemas import Supplier; print(Supplier.__table__.columns.keys())'")
