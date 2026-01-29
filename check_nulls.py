from supabase_client import get_client
import json

def check_null_names():
    client = get_client()
    res = client.table('rolling_hours').select('name').eq('name', None).execute()
    print(f"Found {len(res.data)} records with NULL name")
    
    # Also check if any are string 'None'
    res2 = client.table('rolling_hours').select('name').limit(10).execute()
    print(f"Sample names: {[r['name'] for r in res2.data]}")

if __name__ == "__main__":
    check_null_names()
