import supabase_client as db
from collections import defaultdict
import datetime

def normalize_date(date_str):
    if not date_str: return ""
    try:
        parts = date_str.split('/')
        if len(parts) == 3:
            d, m, y = parts
            d = d.zfill(2)
            m = m.zfill(2)
            if len(y) == 4: y = y[2:]
            return f"{d}/{m}/{y}"
    except: pass
    return date_str

def test_merge():
    print("--- Testing Merge Logic for Jan 9th ---")
    
    # 1. Load AIMS Flights from DB
    all_actuals = db.get_fact_actuals()
    jan9_flights = [f for f in all_actuals if "09/01/2026" in f.get('flight_date', '') or "9/1/2026" in f.get('flight_date', '')]
    print(f"Found {len(jan9_flights)} AIMS flights for Jan 9th in DB")
    
    if not jan9_flights:
        # Try format yyyy-mm-dd
        jan9_flights = [f for f in all_actuals if "2026-01-09" in f.get('flight_date', '')]
        print(f"Trying YYYY-MM-DD: Found {len(jan9_flights)} flights")

    # Normalize flights (like load_from_supabase)
    for f in jan9_flights:
        f_date = f.get('flight_date', '')
        # Simple normalization for test
        if '-' in f_date:
            parts = f_date.split('-')
            f['date'] = f"{parts[2]}/{parts[1]}/{parts[0][2:]}"
        else:
            f['date'] = normalize_date(f_date)
            
    # 2. Load Leg Members from DB
    # We'll check multiple formats explicitly
    leg_formats = ['9/1/2026', '09/01/2026']
    all_legs = []
    for fmt in leg_formats:
        res = db.get_fact_leg_members(filter_date=fmt)
        all_legs.extend(res)
    print(f"Found {len(all_legs)} leg members in DB for Jan 9th (covering {leg_formats})")

    # 3. Build legs_map
    legs_map = defaultdict(list)
    for leg in all_legs:
        l_date = normalize_date(leg.get('leg_date', ''))
        f_no = leg.get('flight_no', '')
        legs_map[(l_date, f_no)].append(leg)
    
    print(f"Built legs_map with {len(legs_map)} keys")
    if legs_map:
        print(f"Sample key: {list(legs_map.keys())[0]}")

    # 4. Perform Merge
    merge_count = 0
    for f in jan9_flights:
        f_date = f.get('date', '')
        f_no = f.get('flight_no', '')
        
        # Try logic
        legs = legs_map.get((f_date, f_no))
        if not legs:
            if f_no.isdigit():
                 legs = legs_map.get((f_date, f"VJ{f_no}"))
            elif f_no.startswith('VJ'):
                 legs = legs_map.get((f_date, f_no[2:]))
        
        if legs:
            merge_count += 1
            if merge_count == 1:
                print(f"DEBUG: First successful merge for flight {f_no} on {f_date}")
                print(f"DEBUG: Found {len(legs)} crew members")

    print(f"Total merged flights: {merge_count} out of {len(jan9_flights)}")

if __name__ == "__main__":
    if db.is_connected():
        test_merge()
    else:
        print("Not connected to Supabase")
