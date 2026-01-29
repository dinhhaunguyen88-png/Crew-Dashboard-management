import os
import sys
import logging
from datetime import datetime
from aims_soap_client import AIMSSoapClient
import json

# Setup basic logging to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('InspectAIMS')

def safe_serialize(obj):
    """Recursively convert Zeep objects to dicts for printing"""
    if hasattr(obj, '__dict__'):
        return safe_serialize(obj.__dict__)
    if isinstance(obj, list):
        return [safe_serialize(x) for x in obj]
    return obj

def inspect_aims_structure():
    print("="*60)
    print("AIMS RAW DATA INSPECTION")
    print("="*60)
    
    client = AIMSSoapClient()
    
    if not client.is_configured():
        print("ERROR: credentials not configured in .env")
        return

    # Use today's date
    today = datetime.now()
    print(f"Fetching data for: {today.date()}")
    
    try:
        # We want to use the internal method _init_client to get access to raw service if needed,
        # but calling the public method is safer to see what the app sees.
        # However, we want to inspect the RAW zeep object before it gets parsed by our client code.
        # So let's monkey-patch or just copy the logic effectively.
        
        client._init_client()
        parts = client._format_date_parts(today)
        
        print("\n[1] Calling FetchLegMembersPerDay...")
        response = client._service.FetchLegMembersPerDay(
            UN=client.username,
            PSW=client.password,
            DD=parts['DD'],
            MM=parts['MM'],
            YY=parts['YYYY']
        )
        
        print("\n[2] Response Top Level Keys:")
        print(dir(response))
        
        # Drill down
        if hasattr(response, 'DayMember'):
            day_mem = response.DayMember
            print(f"\n[3] DayMember found. Type: {type(day_mem)}")
            
            legs = getattr(day_mem, 'TAIMSGetLegMembers', [])
            if not isinstance(legs, list):
                legs = [legs]
                
            print(f"Found {len(legs)} legs.")
            
            if len(legs) > 0:
                print("\n[4] Inspecting First Leg Structure:")
                leg = legs[0]
                # Print all attributes of the first leg
                for attr in dir(leg):
                    if not attr.startswith('_'):
                        val = getattr(leg, attr)
                        if not callable(val):
                            print(f"   - {attr}: {val}")
                
                # Check Crew Members specifically
                f_member = getattr(leg, 'FMember', None)
                if f_member:
                    print("\n[5] Inspecting FMember (Crew) Structure:")
                    crew_list = getattr(f_member, 'TAIMSMember', [])
                    if not isinstance(crew_list, list):
                        crew_list = [crew_list]
                    
                    print(f"   Found {len(crew_list)} crew members in this leg.")
                    if len(crew_list) > 0:
                        crew = crew_list[0]
                        print("   First Crew Member Attributes:")
                        for attr in dir(crew):
                            if not attr.startswith('_'):
                                val = getattr(crew, attr)
                                if not callable(val):
                                    print(f"      - {attr}: {val}")
                else:
                    print("   [WARNING] No FMember found in first leg.")
            else:
                print("   [WARNING] No legs found to inspect.")
        else:
            print("   [WARNING] DayMember NOT found in response.")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_aims_structure()
