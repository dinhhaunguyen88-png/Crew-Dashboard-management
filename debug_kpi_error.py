from data_processor import get_processor
import traceback

def debug_error():
    try:
        processor = get_processor()
        print("Got processor. Calculating metrics for AIMS...")
        data = processor.get_dashboard_data(filter_date=None, source='aims')
        print("Success!")
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    debug_error()
