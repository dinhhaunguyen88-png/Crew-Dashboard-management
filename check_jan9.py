from supabase_client import get_client
import sys

def check_jan_9():
    print("Checking Supabase for Jan 9th 2026 data...")
    client = get_client()
    
    # Check flight count
    try:
        flights = client.table('fact_actuals').select('*', count='exact').eq('flight_date', '09/01/2026').execute()
        f_count = len(flights.data)
        print(f"Flights for 09/01/2026: {f_count}")
    except Exception as e:
        print(f"Error checking flights: {e}")
        
    # Check leg members count with variations
    formats_to_check = ['09/01/2026', '9/1/2026', '09/1/2026', '9/01/2026']
    
    for fmt in formats_to_check:
        try:
            legs = client.table('fact_leg_members').select('*', count='exact').eq('leg_date', fmt).execute()
            c_count = len(legs.data)
            print(f"Crew Legs for '{fmt}': {c_count}")
        except Exception as e:
            print(f"Error checking '{fmt}': {e}")
            
    # Also check Jan 8
    print("-" * 20)
    print("Checking Jan 8th:")
    formats_8 = ['08/01/2026', '8/1/2026', '08/1/2026']
    for fmt in formats_8:
        try:
           legs = client.table('fact_leg_members').select('*', count='exact').eq('leg_date', fmt).execute()
           print(f"Crew Legs for '{fmt}': {len(legs.data)}")
        except: pass

if __name__ == "__main__":
    check_jan_9()
