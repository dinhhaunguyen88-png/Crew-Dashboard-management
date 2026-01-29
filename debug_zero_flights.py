from data_processor import get_processor
import json

processor = get_processor()

# Force load if not already loaded (though get_processor should do it)
if not processor.aims_flights:
    print("re-loading from supabase...")
    processor.load_from_supabase()

print(f"Total AIMS Flights loaded: {len(processor.aims_flights)}")

if processor.aims_flights:
    sample = processor.aims_flights[0]
    print("\n--- Sample Flight Object ---")
    print(json.dumps(sample, indent=2, default=str))

    # Check date formats
    dates = set(f.get('date') or f.get('flight_date') for f in processor.aims_flights[:100])
    print(f"\nSample Dates: {list(dates)[:5]}")

    # Test calculate_metrics with AIMS flights manually
    # Simulate what get_dashboard_data does
    processor.flights = processor.aims_flights
    processor.flights_by_date = processor.aims_flights_by_date
    
    print("\n--- Testing calculate_metrics() ---")
    metrics = processor.calculate_metrics()
    print("Summary:", json.dumps(metrics['summary'], indent=2))
else:
    print("No AIMS flights found.")
