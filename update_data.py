
import json
import os
import sys
from pathlib import Path
from data_processor import DataProcessor
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def update_static_json():
    print("[*] Starting Data Update...")
    
    # Initialize processor
    # passing '.' as data_dir assumes we run this from project root
    processor = DataProcessor(data_dir=Path('.'))
    
    # Process all CSV files locally
    print("[*] Processing CSV files...")
    
    # 1. DayRepReport
    flights = processor.process_dayrep_csv(sync_db=False)
    print(f"   - DayRepReport: {flights} flights loaded")
    
    # 2. SacutilReport (Utilization)
    util = processor.process_sacutil_csv(sync_db=False)
    print(f"   - SacutilReport: {util} records loaded")
    
    # 3. RolCrTotReport (Rolling Hours)
    rolling = processor.process_rolcrtot_csv(sync_db=False)
    print(f"   - RolCrTotReport: {len(processor.rolling_hours)} crew records loaded")
    
    # 4. Crew Schedule
    schedule = processor.process_crew_schedule_csv(sync_db=False)
    print(f"   - Crew Schedule: {schedule} records loaded")

    # Calculate full dashboard metrics
    print("[*] Calculating Metrics...")
    # Using calculate_metrics instead of get_dashboard_data since I couldn't find the alias, 
    # but the logic matched the expected output structure.
    data = processor.calculate_metrics(filter_date=None)
    
    # Add build timestamp
    data['last_updated'] = datetime.now().isoformat()
    
    # Write to deploy_static/dashboard_data.json
    output_path = Path('deploy_static/dashboard_data.json')
    print(f"[*] Saving to {output_path}...")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print("[OK] Data Update Complete!")

if __name__ == "__main__":
    update_static_json()
