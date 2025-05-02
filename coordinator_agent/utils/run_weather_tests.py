#!/usr/bin/env python3
"""
Run both weather test scripts in sequence.
This script helps to test both the OpenWeatherMap API and the weather module implementation.
"""

import os
import sys
import subprocess
import time

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def run_script(script_name):
    """Run a Python script and return the exit code."""
    print_header(f"Running {script_name}")
    
    try:
        # Construct the full path to the script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        
        # Run the script
        result = subprocess.run([sys.executable, script_path], check=False)
        
        if result.returncode == 0:
            print(f"\n✅ {script_name} completed successfully!")
        else:
            print(f"\n❌ {script_name} failed with exit code {result.returncode}")
        
        return result.returncode
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {str(e)}")
        return 1

def main():
    """Main function to run both test scripts."""
    print_header("WEATHER TEST RUNNER")
    
    print("This script will run two tests in sequence:")
    print("1. test_weather_api.py - Tests the OpenWeatherMap API directly")
    print("2. test_weather_module.py - Tests the weather module implementation")
    print("\nNote: Make sure your OpenWeatherMap API key is set in the .env file.")
    
    # Check for .env file in coordinator_agent directory (parent of utils)
    coordinator_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(coordinator_dir, '.env')
    
    print(f"Looking for .env file in: {coordinator_dir}")
    
    if os.path.exists(env_path):
        print(f"✅ Found .env file at: {env_path}")
        
        # Print the directory containing the .env file to help with debugging
        print(f"Directory with .env: {os.path.dirname(env_path)}")
        
        # Set the COORDINATOR_DIR environment variable to help child scripts
        os.environ['COORDINATOR_DIR'] = coordinator_dir
    else:
        print(f"⚠️ No .env file found at: {env_path}")
        print("The tests may still work if the OPENWEATHERMAP_API_KEY environment variable is set.")
    
    input("\nPress Enter to start the tests...")
    
    # Run the API test
    api_test_result = run_script("test_weather_api.py")
    
    # If the API test failed, ask if the user wants to continue
    if api_test_result != 0:
        print("\n⚠️ The API test failed. This may indicate an issue with your API key.")
        choice = input("Do you want to continue with the module test? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting test runner.")
            return
    
    print("\nWaiting 2 seconds before running the next test...")
    time.sleep(2)
    
    # Run the module test
    module_test_result = run_script("test_weather_module.py")
    
    # Final summary
    print_header("TEST SUMMARY")
    print("API Test Result:", "✅ PASSED" if api_test_result == 0 else "❌ FAILED")
    print("Module Test Result:", "✅ PASSED" if module_test_result == 0 else "❌ FAILED")
    
    if api_test_result != 0 or module_test_result != 0:
        print("\n⚠️ One or more tests failed. Please check the test output for details.")
        print("Common issues:")
        print("- Invalid or inactive API key")
        print("- API key not properly set in the .env file")
        print("- Network connectivity issues")
        print("\nSee WEATHER_API_SETUP.md for more information.")
    else:
        print("\n🎉 All tests passed successfully!")

if __name__ == "__main__":
    main() 