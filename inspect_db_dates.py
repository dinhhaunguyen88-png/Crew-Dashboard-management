from supabase_client import get_client
import sys

def inspect_dates():
    print("Inspecting distinct dates in fact_leg_members...")
    client = get_client()
    
    try:
        # Fetch a sample of rows to see the date format
        res = client.table('fact_leg_members').select('leg_date').limit(50).order('synced_at', desc=True).execute()
        
        dates = set()
        for row in res.data:
            dates.add(row['leg_date'])
            
        print(f"Found {len(dates)} distinct dates in recent 50 records:")
        for d in dates:
            print(f" - '{d}'")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_dates()
