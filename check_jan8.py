from supabase_client import get_client
import sys

def check_jan_8():
    print("Checking Supabase for Jan 8th 2026 data...")
    client = get_client()
    
    # Check flight count
    try:
        flights = client.table('fact_actuals').select('*', count='exact').eq('flight_date', '08/01/2026').execute()
        f_count = len(flights.data)
        print(f"Flights for 08/01/2026: {f_count}")
        
        # Check leg members count
        legs = client.table('fact_leg_members').select('*', count='exact').eq('leg_date', '08/01/2026').execute()
        c_count = len(legs.data)
        print(f"Crew Legs for 08/01/2026: {c_count}")
        
        if c_count > 0:
            print("✅ Data exists in DB for Jan 8.")
        else:
            print("❌ Data missing in DB for Jan 8.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_jan_8()
