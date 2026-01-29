from data_processor import DataProcessor
import sys

def debug_logic():
    print("Initializing DataProcessor...")
    processor = DataProcessor()
    
    # Reset data
    processor.flights = []
    processor.aims_flights = []
    processor.rolling_hours = []
    processor.crew_to_regs = {}
    processor.aims_crew_to_regs = {}
    
    print("Test 1: Check ValueError with Empty Crew but Existing Flights")
    processor.flights = [{'flight_no': 'TEST'}]
    
    try:
        print("Calling calculate_compliance_rate_metric...")
        processor.calculate_compliance_rate_metric()
        print("❌ FAILED: ValueError NOT raised")
    except ValueError as e:
        print(f"✅ PASSED: ValueError raised as expected: {e}")
    except Exception as e:
        print(f"❌ FAILED: Wrong exception raised: {type(e)} {e}")

    print("-" * 20)
    
    print("Test 2: Check Success with Data")
    # Reset
    processor.flights = []
    processor.rolling_hours = [{'crew_id': '1', 'hours_28day': 50}]
    try:
        rate = processor.calculate_compliance_rate_metric()
        print(f"✅ PASSED: Calculation successful. Rate: {rate}")
    except Exception as e:
         print(f"❌ FAILED: Exception raised: {e}")

if __name__ == "__main__":
    debug_logic()
