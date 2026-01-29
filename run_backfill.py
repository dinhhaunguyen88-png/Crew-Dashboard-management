import sys
import datetime
from etl_scheduler import get_scheduler
from aims_soap_client import get_aims_client

def backfill_jan_2026():
    print("Initializing Backfill...")
    scheduler = get_scheduler()
    client = get_aims_client()
    
    # Define range: Jan 1, 2026 to Jan 31, 2026
    start_date = datetime.date(2026, 1, 1)
    end_date = datetime.date(2026, 1, 31)
    
    current = start_date
    print(f"Starting backfill from {start_date} to {end_date}...")
    
    while current <= end_date:
        print(f"Syncing crew for {current}...", end='', flush=True)
        try:
            # Fetch
            result = client.fetch_leg_members_per_day(current)
            if result and result.get('success'):
                legs = result.get('legs', [])
                # Sync
                if legs:
                    scheduler._sync_leg_members_to_supabase(legs, current)
                    print(f" [OK] ({len(legs)} records)")
                else:
                    print(f" [OK] (0 records)")
            else:
                print(f" [ERR] AIMS Error: {result.get('error')}")
        except Exception as e:
            print(f" [ERR] Error: {e}")
        
        current += datetime.timedelta(days=1)
        
    print("\nBackfill Complete!")

if __name__ == "__main__":
    backfill_jan_2026()
