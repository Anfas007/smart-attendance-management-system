#!/usr/bin/env python3
"""
Test script to verify DD/MM/YYYY date parsing works correctly
"""
from datetime import datetime

def test_date_parsing():
    """Test parsing DD/MM/YYYY format dates"""
    test_dates = [
        "25/12/1990",  # Valid date
        "01/01/2000",  # Valid date
        "31/12/2023",  # Valid date
        "29/02/2024",  # Valid leap year date
        "32/12/2023",  # Invalid day
        "13/13/2023",  # Invalid month
        "25/12/abc",   # Invalid year
        "25-12-1990",  # Wrong separator
    ]

    print("Testing DD/MM/YYYY date parsing:")
    print("=" * 40)

    for date_str in test_dates:
        try:
            parsed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
            print(f"✓ '{date_str}' -> {parsed_date}")
        except ValueError as e:
            print(f"✗ '{date_str}' -> Error: {e}")

if __name__ == "__main__":
    test_date_parsing()