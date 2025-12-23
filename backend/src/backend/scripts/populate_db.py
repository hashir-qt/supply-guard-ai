import sys
import os

# Add the src directory to Python path to allow imports from backend
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from sqlmodel import Session, select
from backend.database import engine, init_db
from backend.models.schemas import Supplier, Outlet, DeliveryRoute, Risk, CalendarEvent, HistoricalIncident
from backend.data.generator import (
    generate_suppliers, generate_outlets, generate_routes, 
    generate_risks, generate_events, generate_history
)

def populate():
    print("Initializing Database...")
    init_db()
    
    with Session(engine) as session:
        # Check if data exists
        existing_suppliers = session.exec(select(Supplier)).first()
        if existing_suppliers:
            print("Data already exists. Skipping population.")
            return

        print("Generating Data...")
        suppliers = generate_suppliers()
        outlets = generate_outlets()
        routes = generate_routes()
        risks = generate_risks()
        events = generate_events()
        history = generate_history()

        print(f"Adding {len(suppliers)} Suppliers...")
        session.add_all(suppliers)
        
        print(f"Adding {len(outlets)} Outlets...")
        session.add_all(outlets)
        
        print(f"Adding {len(routes)} Routes...")
        session.add_all(routes)
        
        print(f"Adding {len(risks)} Risks...")
        session.add_all(risks)
        
        print(f"Adding {len(events)} Events...")
        session.add_all(events)
        
        print(f"Adding {len(history)} Historical Incidents...")
        session.add_all(history)

        print("Committing to Neon DB...")
        session.commit()
        print("Done!")

if __name__ == "__main__":
    populate()
