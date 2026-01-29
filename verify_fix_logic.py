import sys
import unittest
from unittest.mock import MagicMock, patch
import datetime

# Mock dependencies
sys.modules['aims_soap_client'] = MagicMock()
sys.modules['supabase_client'] = MagicMock()

# Import DataProcessor (assuming it can handle mocked db)
from data_processor import DataProcessor

class TestCrewFix(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
        # Reset data
        self.processor.aims_flights = []
        self.processor.rolling_hours = []
        self.processor.crew_to_regs = {}
        self.processor.aims_crew_to_regs = {}

    def test_compliance_rate_calculation(self):
        # Case 1: Empty crew data but existing flights should raise error
        self.processor.flights = [{'flight_no': 'VJ001'}] # Simulate existing flights
        self.processor.crew_to_regs = {}
        with self.assertRaises(ValueError):
             self.processor.calculate_compliance_rate_metric()
        
        # Reset flights for next steps
        self.processor.flights = []
        
        # Case 2: Populated data
        # Add 10 crew: 8 normal (<=85), 1 warning (86-95), 1 critical (>95)
        self.processor.rolling_hours = [
            {'crew_id': '1', 'hours_28day': 50, 'status': 'normal'},
            {'crew_id': '2', 'hours_28day': 80, 'status': 'normal'},
            {'crew_id': '3', 'hours_28day': 90, 'status': 'warning'}, # Warning in old logic (>85)
            {'crew_id': '4', 'hours_28day': 100, 'status': 'critical'} # Critical in old logic (>95)
        ]
        # We need to simulate enough crew to test logic.
        # DataProcessor.calculate_rolling_28day_stats uses:
        # normal_count + warning_count / total
        # warning is > 85, critical is > 95
        
        # In my mock:
        # Crew 3: 90 -> Warning
        # Crew 4: 100 -> Critical
        # Safe crew = Normal + Warning? 
        # checking code: safe_crew = rolling_stats['normal'] + rolling_stats['warning'] (Wait, really?)
        # Let's check the code I saw in view_file step 154 (line 1471):
        # "safe_crew = rolling_stats['normal'] + rolling_stats['warning']"
        # So Critical is the only one that reduces compliance.
        
        stats = self.processor.calculate_compliance_rate_metric()
        print(f"Compliance Rate: {stats}%")
        
        # Expected: 3 safe out of 4 = 75%
        self.assertEqual(stats, 75.0)

    @patch('data_processor.db')
    def test_leg_member_merge(self, mock_db):
        print("\nTesting Leg Member Merge...")
        
        # Setup mock return for flight actuals
        # Note: load_from_supabase calls db.get_fact_actuals()
        mock_db.is_connected.return_value = True
        mock_db.get_fact_actuals.return_value = [
            {'flight_date': '2026-01-30', 'flight_no': 'VJ101', 'dep': 'SGN', 'arr': 'HAN'}, # Will be normalized
        ]
        mock_db.get_ac_utilization.return_value = []
        mock_db.get_rolling_hours.return_value = []
        mock_db.get_crew_schedule.return_value = []
        mock_db.get_standby_records.return_value = []
        
        # Setup mock return for leg members
        mock_db.get_fact_leg_members.return_value = [
            {
                'leg_date': '30/01/2026', # DD/MM/YYYY
                'flight_no': 'VJ101',
                'crew_id': '12345',
                'crew_name': 'NGUYEN VAN A',
                'crew_role': 'CP'
            },
            {
                'leg_date': '30/01/2026',
                'flight_no': 'VJ101',
                'crew_id': '67890',
                'crew_name': 'LE THI B',
                'crew_role': 'FO'
            }
        ]
        
        # Run load_from_supabase
        self.processor.load_from_supabase()
        
        # Check if crew string was constructed in aims_flights
        flight = self.processor.aims_flights[0]
        print(f"Merged Flight Crew String: {flight.get('crew')}")
        
        self.assertTrue('A(CP) 12345' in flight.get('crew', ''))
        self.assertTrue('B(FO) 67890' in flight.get('crew', ''))

if __name__ == '__main__':
    unittest.main()
