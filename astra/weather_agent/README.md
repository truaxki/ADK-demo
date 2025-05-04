# Weather Agent

A specialized sub-agent for Astra that provides real-time weather information.

## Overview

The Weather Agent is a specialized component that handles all weather-related queries. It leverages the OpenWeatherMap API to provide current weather conditions for locations worldwide.

## Setup Requirements

### OpenWeatherMap API Key

This agent requires an OpenWeatherMap API key to function. Follow these steps to set it up:

1. Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/)
2. Generate an API key from your account dashboard
3. Set the API key as an environment variable:

```
OPENWEATHERMAP_API_KEY=your_api_key_here
```

You can set this environment variable in your `.env` file in the main Astra directory.

## Features

- **Get current weather conditions** for any city worldwide
- **Set temperature unit preference** between Celsius and Fahrenheit
- Maintains state regarding user preferences and previous locations

## Available Tools

### get_weather_stateful

Gets current weather information for a specified city.

### set_temperature_unit

Sets the user's preferred temperature unit (Celsius or Fahrenheit).

## Usage Examples

When integrated with Astra, users can ask queries like:

- "What's the weather like in Tokyo?"
- "Tell me the weather in New York"
- "I'd like to use Celsius for temperatures"
- "Switch to Fahrenheit" 