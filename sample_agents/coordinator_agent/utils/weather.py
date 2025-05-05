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
import time
from google.adk.tools.tool_context import ToolContext

# In-memory cache for geocoding results to avoid repeated API calls
geocoding_cache = {}

def geocode_city(city_name):
    """Convert a city name to geographic coordinates using Nominatim.
    
    Args:
        city_name (str): The name of the city to geocode
        
    Returns:
        dict: Location data with coordinates, or None if geocoding failed
    """
    # Check cache first for performance
    cache_key = city_name.lower().strip()
    if cache_key in geocoding_cache:
        return geocoding_cache[cache_key]
    
    # Format city name for the API request
    formatted_city = city_name.strip()
    
    try:
        # Call Nominatim API (OpenStreetMap's geocoding service)
        headers = {"User-Agent": "Coordinator-Agent-Weather-Tool/1.0"}
        params = {
            "q": formatted_city,
            "format": "json",
            "limit": 1,
            "addressdetails": 1
        }
        
        response = requests.get(
            "https://nominatim.openstreetmap.org/search", 
            params=params, 
            headers=headers, 
            timeout=10
        )
        
        # Respect Nominatim's usage policy
        time.sleep(1)
        
        # Handle non-200 responses
        if response.status_code != 200:
            return None
        
        # Parse the response
        data = response.json()
        if not data:
            return None
        
        # Extract location components from the first result
        result = data[0]
        address = result.get("address", {})
        
        # Find the best name for the location
        city = address.get("city", 
               address.get("town", 
               address.get("village", 
               address.get("hamlet", 
               result.get("display_name", "Unknown").split(",")[0]))))
        
        state = address.get("state", address.get("province", None))
        country = address.get("country", "Unknown")
        country_code = address.get("country_code", "").upper()
        
        # Build the location object
        location = {
            "lat": float(result["lat"]),
            "lon": float(result["lon"]),
            "name": city,
            "state": state,
            "country": country,
            "country_code": country_code
        }
        
        # Cache the result for future use
        geocoding_cache[cache_key] = location
        return location
        
    except Exception:
        # Try the fallback for common cities
        fallback_cities = {
            "new york": {"lat": 40.7128, "lon": -74.0060, "name": "New York", "state": "NY", "country": "United States"},
            "london": {"lat": 51.5074, "lon": -0.1278, "name": "London", "state": None, "country": "United Kingdom"},
            "paris": {"lat": 48.8566, "lon": 2.3522, "name": "Paris", "state": None, "country": "France"},
            "tokyo": {"lat": 35.6762, "lon": 139.6503, "name": "Tokyo", "state": None, "country": "Japan"},
            "los angeles": {"lat": 34.0522, "lon": -118.2437, "name": "Los Angeles", "state": "CA", "country": "United States"},
            "charleston": {"lat": 32.7765, "lon": -79.9311, "name": "Charleston", "state": "SC", "country": "United States"}
        }
        
        # Check if the city name contains any of our fallback cities
        for key, value in fallback_cities.items():
            if key in city_name.lower():
                return value
                
        return None

def format_location_name(location):
    """Create a formatted location name from location components.
    
    Args:
        location (dict): Location data with name, state, country
        
    Returns:
        str: Formatted location name (e.g., "New York, NY, US")
    """
    name = location["name"]
    
    if location.get("state"):
        name += f", {location['state']}"
        
    if location.get("country_code"):
        name += f", {location['country_code']}"
    elif location.get("country"):
        name += f", {location['country']}"
        
    return name

def get_weather_data(lat, lon, api_key, units="imperial"):
    """Fetch weather data from OpenWeatherMap API.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        api_key (str): OpenWeatherMap API key
        units (str): Units for temperature (metric/imperial)
        
    Returns:
        dict: Weather data or None if request failed
    """
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": units
        }
        
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params,
            timeout=10
        )
        
        if response.status_code != 200:
            return None
            
        return response.json()
        
    except Exception:
        return None

def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Get weather for a city with temperature unit based on user preference.
    
    Args:
        city (str): City name to get weather for
        tool_context (ToolContext): Context with user preferences
        
    Returns:
        dict: Weather information with status and report
    """
    # Get user's temperature unit preference (default to Fahrenheit)
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Fahrenheit")
    
    # Get API key from environment
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return {
            "status": "error", 
            "error_message": "OpenWeatherMap API key not found in environment variables."
        }
    
    # Convert unit preference to API parameter
    api_units = "imperial" if preferred_unit == "Fahrenheit" else "metric"
    
    # Step 1: Geocode the city name to coordinates
    location = geocode_city(city)
    if not location:
        return {
            "status": "error",
            "error_message": f"Could not find location: '{city}'. Please check the spelling and try again."
        }
    
    # Step 2: Get weather data for the coordinates
    weather_data = get_weather_data(
        location["lat"], 
        location["lon"], 
        api_key, 
        api_units
    )
    
    if not weather_data:
        return {
            "status": "error",
            "error_message": f"Could not retrieve weather data for {city}."
        }
    
    # Step 3: Extract and format the weather information
    try:
        # Get the weather details
        temp = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        
        # Format the location name
        display_name = format_location_name(location)
        
        # Set temperature unit symbol
        temp_unit = "°F" if api_units == "imperial" else "°C"
        speed_unit = "mph" if api_units == "imperial" else "m/s"
        
        # Create the weather report
        report = (
            f"The weather in {display_name} is {condition} with a temperature of "
            f"{temp:.1f}{temp_unit}.\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} {speed_unit}"
        )
        
        # Build the result object
        result = {
            "status": "success", 
            "report": report,
            "data": {
                "city": display_name,
                "coordinates": {
                    "lat": location["lat"],
                    "lon": location["lon"]
                },
                "temperature": temp,
                "temperature_unit": temp_unit,
                "condition": condition,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "wind_speed_unit": speed_unit
            }
        }
        
        # Update the user's state with the last checked location
        tool_context.state["last_city_checked_stateful"] = display_name
        
        return result
        
    except KeyError as e:
        return {
            "status": "error",
            "error_message": f"Missing data in weather response: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error processing weather data: {str(e)}"
        } 