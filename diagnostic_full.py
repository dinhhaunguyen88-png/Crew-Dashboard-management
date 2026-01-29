"""
Comprehensive Test Script for Crew Dashboard
Tests: API connection, CSV upload simulation, data processing, and AIMS integration
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("COMPREHENSIVE DASHBOARD DIAGNOSTIC")
print("=" * 60)

# 1. Test imports
print("\n[1] Checking imports...")
try:
    from data_processor import get_processor, refresh_data
    print("   [OK] data_processor")
except Exception as e:
    print(f"   [FAIL] data_processor: {e}")

try:
    from aims_soap_client import is_aims_available, get_aims_client
    print("   [OK] aims_soap_client")
except Exception as e:
    print(f"   [FAIL] aims_soap_client: {e}")

try:
    import supabase_client as db
    print("   [OK] supabase_client")
except Exception as e:
    print(f"   [FAIL] supabase_client: {e}")

# 2. Test Supabase connection
print("\n[2] Checking Supabase connection...")
if db.is_connected():
    print("   [OK] Supabase CONNECTED")
else:
    print("   [FAIL] Supabase NOT CONNECTED")

# 3. Test AIMS availability
print("\n[3] Checking AIMS API availability...")
if is_aims_available():
    print("   [OK] AIMS API ENABLED and CONFIGURED")
    client = get_aims_client()
    print(f"   - WSDL: {client.wsdl_url}")
    print(f"   - Configured: {client.is_configured()}")
    print(f"   - Enabled: {client.is_enabled()}")
else:
    print("   [WARN] AIMS API NOT AVAILABLE")

# 4. Test DataProcessor initialization
print("\n[4] Testing DataProcessor...")
processor = get_processor()
print(f"   - Total flights: {len(processor.flights)}")
print(f"   - AIMS flights: {len(processor.aims_flights)}")
print(f"   - AIMS available dates: {len(processor.aims_available_dates)}")
print(f"   - AIMS reg_flight_hours sample: {list(processor.aims_reg_flight_hours.items())[:3]}")
print(f"   - Standby records: {len(processor.standby_records)}")

# 5. Test get_dashboard_data with different sources
print("\n[5] Testing get_dashboard_data()...")

# Test CSV source
print("\n   [5a] Source: CSV")
try:
    data_csv = processor.get_dashboard_data(filter_date=None, source='csv')
    print(f"      - total_flights: {data_csv['summary']['total_flights']}")
    print(f"      - total_crew: {data_csv['summary']['total_crew']}")
    print(f"      - total_block_hours: {data_csv['summary']['total_block_hours']}")
except Exception as e:
    print(f"      [FAIL] ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test AIMS source
print("\n   [5b] Source: AIMS")
try:
    data_aims = processor.get_dashboard_data(filter_date=None, source='aims')
    print(f"      - total_flights: {data_aims['summary']['total_flights']}")
    print(f"      - total_crew: {data_aims['summary']['total_crew']}")
    print(f"      - total_block_hours: {data_aims['summary']['total_block_hours']}")
    print(f"      - is_aims_source: {data_aims.get('is_aims_source')}")
except Exception as e:
    print(f"      [FAIL] ERROR: {e}")
    import traceback
    traceback.print_exc()

# 6. Test CSV upload simulation
print("\n[6] Testing CSV upload (simulation)...")
sample_csv = """Date,Flt,Reg,Dep,Arr,STD,STA,Crew
29/01/26,VJ100,VN-A600,SGN,HAN,08:00,10:00,NGUYEN(CP) 1234-LE(FO) 5678
"""
try:
    result = processor.process_dayrep_csv(file_content=sample_csv.encode('utf-8'))
    print(f"   [OK] DayRep processing returned: {result}")
except Exception as e:
    print(f"   [FAIL] DayRep processing FAILED: {e}")
    import traceback
    traceback.print_exc()

# 7. Verify AIMS map population
print("\n[7] Verifying AIMS KPI Maps...")
if hasattr(processor, 'aims_reg_flight_hours') and processor.aims_reg_flight_hours:
    print(f"   [OK] aims_reg_flight_hours: {len(processor.aims_reg_flight_hours)} entries")
else:
    print("   [FAIL] aims_reg_flight_hours is EMPTY or MISSING")

if hasattr(processor, 'aims_flights_by_date') and processor.aims_flights_by_date:
    print(f"   [OK] aims_flights_by_date: {len(processor.aims_flights_by_date)} dates")
else:
    print("   [FAIL] aims_flights_by_date is EMPTY or MISSING")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
