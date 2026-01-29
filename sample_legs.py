from supabase_client import get_client
import json

def sample_data():
    client = get_client()
    res = client.table('fact_leg_members').select('*').limit(5).execute()
    print(json.dumps(res.data, indent=2))

if __name__ == "__main__":
    sample_data()
