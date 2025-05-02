# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import requests
import json
import re
import time
from google.adk.tools.tool_context import ToolContext

# Cache for geocoding results to avoid repeated API calls
# Format: {lowercase_city_name: {"lat": latitude, "lon": longitude, "name": properly_formatted_name}}
geocoding_cache = {}

def geocode_city(city_name):
    """
    Convert a city name to geographic coordinates using the Nominatim geocoding service.
    This service doesn't require an API key and is quite robust for city name lookups.
    
    Args:
        city_name (str): The name of the city to geocode
        
    Returns:
        dict: A dictionary with latitude, longitude, and formatted city name,
              or None if geocoding failed
    """
    # Check cache first
    cache_key = city_name.lower().strip()
    if cache_key in geocoding_cache:
        print(f"--- Tool Debug: Using cached geocoding for '{city_name}' ---")
        return geocoding_cache[cache_key]
    
    # Format city name and prepare API call
    formatted_city = city_name.strip()
    
    try:
        # Using Nominatim (OpenStreetMap) geocoding service
        geocoding_url = "https://nominatim.openstreetmap.org/search"
        headers = {
            # User agent is required by Nominatim's usage policy
            "User-Agent": "Coordinator-Agent-Weather-Tool/1.0"
        }
        params = {
            "q": formatted_city,
            "format": "json",
            "limit": 1,  # Just get the most relevant result
            "addressdetails": 1  # Include address details
        }
        
        print(f"--- Tool Debug: Geocoding city name: '{formatted_city}' using Nominatim ---")
        response = requests.get(geocoding_url, params=params, headers=headers, timeout=10)
        
        # Respect Nominatim usage policy (1 request per second)
        time.sleep(1)
        
        if response.status_code != 200:
            print(f"--- Tool Error: Geocoding API error, status code {response.status_code} ---")
            return None
        
        geocoding_data = response.json()
        
        # Check if we got any results
        if not geocoding_data or len(geocoding_data) == 0:
            print(f"--- Tool Error: No geocoding results for '{formatted_city}' ---")
            return None
        
        # Extract the data - Nominatim format is different from OpenWeatherMap
        first_result = geocoding_data[0]
        address = first_result.get("address", {})
        
        # Try to get the most appropriate name components
        city = address.get("city", address.get("town", address.get("village", address.get("hamlet", None))))
        state = address.get("state", address.get("province", None))
        country = address.get("country", "Unknown")
        country_code = address.get("country_code", "").upper()
        
        # If city is None, use the display name as fallback
        if not city:
            city = first_result.get("display_name", "Unknown").split(",")[0]
        
        # Create result object
        result = {
            "lat": float(first_result["lat"]),
            "lon": float(first_result["lon"]),
            "name": city,
            "country": country,
            "state": state,
            "country_code": country_code,
            "display_name": first_result.get("display_name")
        }
        
        # Store in cache
        geocoding_cache[cache_key] = result
        
        # Log success
        location_name = result["name"]
        if result["state"]:
            location_name += f", {result['state']}"
        location_name += f", {result['country']}"
        
        print(f"--- Tool Debug: Geocoded '{formatted_city}' to coordinates: ({result['lat']}, {result['lon']}) [{location_name}] ---")
        
        return result
    
    except Exception as e:
        print(f"--- Tool Error: Nominatim geocoding error: {str(e)} ---")
        
        # Fallback to simple coordinates if possible
        # This is a very basic fallback for "well-known" cities
        fallback_coords = {
            "new york": {"lat": 40.7128, "lon": -74.0060, "name": "New York", "state": "NY", "country": "United States"},
            "london": {"lat": 51.5074, "lon": -0.1278, "name": "London", "state": None, "country": "United Kingdom"},
            "paris": {"lat": 48.8566, "lon": 2.3522, "name": "Paris", "state": None, "country": "France"},
            "tokyo": {"lat": 35.6762, "lon": 139.6503, "name": "Tokyo", "state": None, "country": "Japan"},
            "los angeles": {"lat": 34.0522, "lon": -118.2437, "name": "Los Angeles", "state": "CA", "country": "United States"},
            "charleston": {"lat": 32.7765, "lon": -79.9311, "name": "Charleston", "state": "SC", "country": "United States"}
        }
        
        # Try to find a key that matches part of the city name
        for key, value in fallback_coords.items():
            if key in city_name.lower():
                print(f"--- Tool Debug: Using fallback coordinates for '{city_name}' based on match with '{key}' ---")
                return value
                
        return None

def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather from OpenWeatherMap API, converts temp unit based on session state.
    
    Args:
        city (str): The name of the city to get weather for
        tool_context (ToolContext): Context containing session state
        
    Returns:
        dict: A dictionary containing the weather information
    """
    print(f"--- Tool: get_weather_stateful called for {city} ---")

    # --- Read preference from state ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # Default to Celsius
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    # Get API key from environment variables
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        error_msg = "OpenWeatherMap API key not found. Please set the OPENWEATHERMAP_API_KEY environment variable."
        print(f"--- Tool Error: {error_msg} ---")
        return {"status": "error", "error_message": error_msg}
    
    # Set units parameter for API call based on user preference
    api_units = "metric"  # Default to metric (Celsius)
    if preferred_unit == "Fahrenheit":
        api_units = "imperial"
    
    # First, geocode the city name to get coordinates
    geo_data = geocode_city(city)
    
    if not geo_data:
        error_msg = f"Could not find coordinates for location: '{city}'. Please check the spelling and try again."
        print(f"--- Tool Error: {error_msg} ---")
        return {"status": "error", "error_message": error_msg}
    
    # Make the API call with coordinates
    try:
        # Base URL for the current weather API
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        # Build parameters with coordinates
        params = {
            "lat": geo_data["lat"],
            "lon": geo_data["lon"],
            "appid": api_key,
            "units": api_units
        }
        
        # Log the request parameters (masking the API key)
        masked_params = {k: v if k != 'appid' else '***' for k, v in params.items()}
        print(f"--- Tool Debug: Making request to {base_url} with params: {json.dumps(masked_params)} ---")
        
        # Make the API request
        response = requests.get(base_url, params=params, timeout=10)
        
        # Debug log
        print(f"--- Tool Debug: Response status code: {response.status_code} ---")
        
        # Handle HTTP errors
        if response.status_code != 200:
            # Try to parse the error message from the response
            try:
                error_data = response.json()
                error_code = error_data.get('cod', response.status_code)
                error_message = error_data.get('message', 'Unknown error')
                
                # Handle specific error codes
                if error_code == 401:
                    error_msg = f"Authentication failed: Invalid API key. Please check your OpenWeatherMap API key."
                elif error_code == 404:
                    error_msg = f"Weather data not available for '{city}' at the coordinates ({geo_data['lat']}, {geo_data['lon']})."
                elif error_code == 429:
                    error_msg = "API rate limit exceeded. Too many requests have been made."
                else:
                    error_msg = f"API Error {error_code}: {error_message}"
                
                print(f"--- Tool Error: {error_msg} ---")
                return {"status": "error", "error_message": error_msg}
            except:
                # Fallback for non-JSON responses
                error_msg = f"HTTP Error: {response.status_code}"
                print(f"--- Tool Error: {error_msg} ---")
                return {"status": "error", "error_message": error_msg}
        
        # Parse the JSON response
        weather_data = response.json()
        
        # Debug log of full response for troubleshooting
        print(f"--- Tool Debug: Weather data received: {json.dumps(weather_data)} ---")
        
        # Extract relevant weather information
        temp = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        
        # Set temperature unit symbol based on selected units
        temp_unit = "°C" if api_units == "metric" else "°F"
        
        # Format display name using geocoding data for more accuracy
        display_name = geo_data["name"]
        if geo_data.get("state"):
            display_name += f", {geo_data['state']}"
        if geo_data.get("country_code"):
            display_name += f", {geo_data['country_code']}"
        elif geo_data.get("country"):
            display_name += f", {geo_data['country']}"
        
        # Create detailed weather report
        report = (
            f"The weather in {display_name} is {condition} with a temperature of "
            f"{temp:.1f}{temp_unit}.\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} " + ("m/s" if api_units == "metric" else "mph")
        )
        
        result = {
            "status": "success", 
            "report": report,
            "data": {
                "city": display_name,
                "coordinates": {
                    "lat": geo_data["lat"],
                    "lon": geo_data["lon"]
                },
                "temperature": temp,
                "temperature_unit": temp_unit,
                "condition": condition,
                "humidity": humidity,
                "wind_speed": wind_speed
            }
        }
        
        print(f"--- Tool: Generated weather report for {display_name}. ---")
        
        # Update state with last checked city
        tool_context.state["last_city_checked_stateful"] = display_name
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {display_name} ---")
        
        return result
        
    except requests.exceptions.Timeout:
        error_msg = "Request timed out. The weather service might be slow or unavailable."
        print(f"--- Tool Error: {error_msg} ---")
        return {"status": "error", "error_message": error_msg}
        
    except requests.exceptions.ConnectionError:
        error_msg = "Connection error. Please check your internet connection."
        print(f"--- Tool Error: {error_msg} ---")
        return {"status": "error", "error_message": error_msg}
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to weather service: {str(e)}"
        print(f"--- Tool Error: {error_msg} ---")
        return {"status": "error", "error_message": error_msg}
    
    except KeyError as e:
        error_msg = f"Data format error: Missing expected field '{str(e)}' in weather data."
        print(f"--- Tool Error: {error_msg} ---")
        return {"status": "error", "error_message": error_msg}
        
    except Exception as e:
        error_msg = f"Unexpected error getting weather data: {str(e)}"
        print(f"--- Tool Error: {error_msg} ---")
        return {"status": "error", "error_message": error_msg} 