"""
Supabase Client Module for Crew Dashboard
Handles database operations for storing and retrieving CSV data
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None

def init_supabase():
    """Initialize Supabase client"""
    global supabase
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return True
    return False

def get_client() -> Client:
    """Get initialized Supabase client"""
    global supabase
    if supabase is None:
        init_supabase()
    return supabase


# ==================== FLIGHTS TABLE ====================

def insert_flights(flights_data: list):
    """Insert flight records from DayRepReport CSV"""
    client = get_client()
    if not client:
        return None
    
    # Clear existing data before insert
    client.table('flights').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    
    # Insert new data in batches of 500
    batch_size = 500
    for i in range(0, len(flights_data), batch_size):
        batch = flights_data[i:i+batch_size]
        client.table('flights').insert(batch).execute()
    
    return len(flights_data)

def get_flights(filter_date: str = None):
    """Get flights, optionally filtered by date"""
    client = get_client()
    if not client:
        return []
    
    query = client.table('flights').select('*')
    if filter_date:
        query = query.eq('date', filter_date)
    
    result = query.execute()
    return result.data if result.data else []

def get_available_dates():
    """Get list of unique dates from flights"""
    client = get_client()
    if not client:
        return []
    
    result = client.table('flights').select('date').execute()
    if result.data:
        dates = list(set([r['date'] for r in result.data]))
        # Sort dates chronologically
        dates.sort(key=lambda d: tuple(map(int, d.split('/')[::-1])))
        return dates
    return []


# ==================== AC UTILIZATION TABLE ====================

def insert_ac_utilization(util_data: list):
    """Insert AC utilization records from SacutilReport CSV"""
    client = get_client()
    if not client:
        return None
    
    # Clear existing data
    client.table('ac_utilization').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    
    # Insert new data
    batch_size = 500
    for i in range(0, len(util_data), batch_size):
        batch = util_data[i:i+batch_size]
        client.table('ac_utilization').insert(batch).execute()
    
    return len(util_data)

def get_ac_utilization(filter_date: str = None):
    """Get AC utilization, optionally filtered by date"""
    client = get_client()
    if not client:
        return []
    
    query = client.table('ac_utilization').select('*')
    if filter_date:
        query = query.eq('date', filter_date)
    
    result = query.execute()
    return result.data if result.data else []


# ==================== ROLLING HOURS TABLE ====================

def insert_rolling_hours(hours_data: list):
    """Insert rolling hours records from RolCrTotReport CSV"""
    client = get_client()
    if not client:
        return None
    
    # Clear existing data
    client.table('rolling_hours').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    
    # Insert new data
    batch_size = 500
    for i in range(0, len(hours_data), batch_size):
        batch = hours_data[i:i+batch_size]
        client.table('rolling_hours').insert(batch).execute()
    
    return len(hours_data)

def get_rolling_hours():
    """Get all rolling hours data"""
    client = get_client()
    if not client:
        return []
    
    result = client.table('rolling_hours').select('*').order('hours_28day', desc=True).execute()
    return result.data if result.data else []


# ==================== CREW SCHEDULE TABLE ====================

def insert_crew_schedule(schedule_data: list):
    """Insert crew schedule records from Crew Schedule CSV"""
    client = get_client()
    if not client:
        return None
    
    # Clear existing data
    client.table('crew_schedule').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
    
    # Insert new data
    batch_size = 500
    for i in range(0, len(schedule_data), batch_size):
        batch = schedule_data[i:i+batch_size]
        client.table('crew_schedule').insert(batch).execute()
    
    return len(schedule_data)

def get_crew_schedule(filter_date: str = None):
    """Get crew schedule, optionally filtered by date"""
    client = get_client()
    if not client:
        return []
    
    query = client.table('crew_schedule').select('*')
    if filter_date:
        query = query.eq('date', filter_date)
    
    result = query.execute()
    return result.data if result.data else []

def get_crew_schedule_summary(filter_date: str = None):
    """Get summary counts of crew schedule statuses"""
    data = get_crew_schedule(filter_date)
    summary = {'SL': 0, 'CSL': 0, 'SBY': 0, 'OSBY': 0}
    for record in data:
        status = record.get('status_type', '')
        if status in summary:
            summary[status] += 1
    return summary


# ==================== UTILITY FUNCTIONS ====================

def check_connection():
    """Check if Supabase connection is working"""
    client = get_client()
    if not client:
        return False, "Supabase credentials not configured"
    
    try:
        # Try to query flights table
        result = client.table('flights').select('id').limit(1).execute()
        return True, "Connected successfully"
    except Exception as e:
        return False, str(e)

def clear_all_data():
    """Clear all data from all tables"""
    client = get_client()
    if not client:
        return False
    
    tables = ['flights', 'ac_utilization', 'rolling_hours', 'crew_schedule']
    for table in tables:
        try:
            client.table(table).delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        except:
            pass
    return True
