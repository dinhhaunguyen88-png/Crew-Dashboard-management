"""
Deep Debug Script - Test actual request flow
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("DEEP DEBUG: Testing Request Flow")
print("=" * 60)

from data_processor import get_processor

processor = get_processor()

print(f"\n[1] DataProcessor State:")
print(f"    - processor.flights length: {len(processor.flights)}")
print(f"    - processor.aims_flights length: {len(processor.aims_flights)}")

# Simulate the auto-detection logic
print(f"\n[2] Auto-Detection Logic:")
if len(processor.flights) == 0 and len(processor.aims_flights) > 0:
    source = 'aims'
    print(f"    -> AUTO-DETECTED: source = 'aims' (CSV empty, AIMS has data)")
else:
    source = 'csv'
    print(f"    -> source = 'csv' (CSV has {len(processor.flights)} flights)")

# Test get_dashboard_data with auto-detected source
print(f"\n[3] Testing get_dashboard_data with source='{source}':")
data = processor.get_dashboard_data(filter_date=None, source=source)
print(f"    - is_aims_source: {data.get('is_aims_source')}")
print(f"    - total_flights: {data['summary']['total_flights']}")
print(f"    - total_aircraft: {data['summary']['total_aircraft']}")
print(f"    - total_block_hours: {data['summary']['total_block_hours']}")
print(f"    - available_dates count: {len(data.get('available_dates', []))}")

# Check if flights table has any data in Supabase
print(f"\n[4] Checking Supabase flights table:")
import supabase_client as db
if db.is_connected():
    flights_db = db.get_flights()
    print(f"    - Supabase flights table: {len(flights_db) if flights_db else 0} records")
else:
    print("    - Supabase not connected")

# Check the flights table specifically
print(f"\n[5] Checking processor.flights content:")
if processor.flights:
    print(f"    - First flight sample: {processor.flights[0]}")
else:
    print(f"    - processor.flights is EMPTY")

print("\n" + "=" * 60)
print("DEEP DEBUG COMPLETE")
print("=" * 60)
