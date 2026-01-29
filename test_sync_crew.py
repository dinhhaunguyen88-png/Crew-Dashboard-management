import sys
import datetime
from etl_scheduler import get_scheduler

def sync_one_day():
    print("Initializing Scheduler...")
    scheduler = get_scheduler()
    
    # Specific day to sync (e.g., yesterday or today)
    target_date = datetime.date.today()
    print(f"Syncing crew data for {target_date}...")
    
    # Manually fetch and sync for one day
    try:
        from aims_soap_client import get_aims_client
        client = get_aims_client()
        
        # Fetch leg members for this day
        print(f"Fetching leg members for {target_date}...")
        result = client.fetch_leg_members_per_day(target_date)
        
        if result and isinstance(result, list):
            print(f"Fetched {len(result)} leg members.")
            # Sync to Supabase
            print("Syncing to Supabase...")
            scheduler._sync_leg_members_to_supabase(result, target_date)
            print("✅ Single day crew sync completed successfully.")
        else:
             print("⚠️ No leg members found or error fetching.")
             
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_one_day()
