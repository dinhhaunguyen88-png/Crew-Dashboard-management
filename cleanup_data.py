import datetime
from etl_scheduler import ETLScheduler
from aims_soap_client import get_aims_client

def cleanup_day(day_str):
    client = get_aims_client()
    scheduler = ETLScheduler()
    
    target_date = datetime.datetime.strptime(day_str, "%d/%m/%Y")
    print(f"Cleaning and re-syncing {day_str}...")
    
    res = client.fetch_leg_members_per_day(target_date)
    if res.get('success'):
        legs = res.get('legs', [])
        scheduler._sync_leg_members_to_supabase(legs, target_date)
        print(f"Successfully cleaned and synced {len(legs)} legs.")
    else:
        print(f"Error fetching data: {res.get('error')}")

if __name__ == "__main__":
    cleanup_day("09/01/2026")
    cleanup_day("01/01/2026") # Also clean first day
    cleanup_day("08/01/2026") # And Jan 8
