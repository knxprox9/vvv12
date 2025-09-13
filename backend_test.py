#!/usr/bin/env python3
"""
Backend API Test Suite
Tests the FastAPI backend endpoints using requests library
"""

import requests
import sys
import json
from datetime import datetime

class BackendAPITester:
    def __init__(self, base_url="http://127.0.0.1:8001"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)}")
                    return True, response_data
                except:
                    print(f"   Response: {response.text}")
                    return True, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test GET /api/ endpoint"""
        success, response = self.run_test(
            "Root Endpoint",
            "GET",
            "api/",
            200
        )
        if success and isinstance(response, dict) and response.get('message') == 'Hello World':
            print("   ✓ Correct message returned")
            return True
        else:
            print("   ✗ Incorrect response format or message")
            return False

    def test_create_status_check(self):
        """Test POST /api/status endpoint"""
        test_data = {"client_name": "deep-test"}
        success, response = self.run_test(
            "Create Status Check",
            "POST",
            "api/status",
            200,
            data=test_data
        )
        
        if success and isinstance(response, dict):
            # Validate response structure
            required_fields = ['id', 'client_name', 'timestamp']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"   ✗ Missing fields: {missing_fields}")
                return False, None
            
            if response['client_name'] != 'deep-test':
                print(f"   ✗ Incorrect client_name: {response['client_name']}")
                return False, None
                
            print("   ✓ All required fields present and correct")
            return True, response['id']
        
        return False, None

    def test_get_status_checks(self):
        """Test GET /api/status endpoint"""
        success, response = self.run_test(
            "Get Status Checks",
            "GET",
            "api/status",
            200
        )
        
        if success and isinstance(response, list):
            if len(response) >= 1:
                # Check if our test entry exists
                deep_test_entries = [item for item in response if item.get('client_name') == 'deep-test']
                if deep_test_entries:
                    print(f"   ✓ Found {len(deep_test_entries)} 'deep-test' entries")
                    return True
                else:
                    print("   ✗ No 'deep-test' entries found")
                    return False
            else:
                print("   ✗ Empty response array")
                return False
        else:
            print("   ✗ Response is not a list")
            return False

def main():
    """Main test runner"""
    print("🚀 Starting Backend API Tests")
    print("=" * 50)
    
    tester = BackendAPITester()
    
    # Test 1: Root endpoint
    test1_passed = tester.test_root_endpoint()
    
    # Test 2: Create status check
    test2_passed, status_id = tester.test_create_status_check()
    
    # Test 3: Get status checks
    test3_passed = tester.test_get_status_checks()
    
    # Print final results
    print("\n" + "=" * 50)
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())