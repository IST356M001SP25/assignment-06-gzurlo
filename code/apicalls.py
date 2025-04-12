import requests
from typing import Dict, Any

# Put your CENT Ischool IoT Portal API KEY here.
APIKEY = "cc31ccceba0688279f2d0aaf"

def get_google_place_details(google_place_id: str) -> Dict[str, Any]:
    """
    Fetch place details including reviews from Google Places API.
    
    Args:
        google_place_id: The Google Place ID to look up
        
    Returns:
        Dictionary containing place details and reviews
        Format: {'result': {place_details}, 'status': 'OK'}
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    headers = {'X-API-KEY': APIKEY}
    params = {'place_id': google_place_id}
    url = "https://cent.ischool-iot.net/api/google/place/details"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google Place details: {e}")
        return {'error': str(e), 'status': 'REQUEST_FAILED'}

def get_azure_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze text sentiment using Azure Text Analytics.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing sentiment analysis results
        Format: {'documents': [sentiment_results], 'errors': []}
    """
    headers = {
        'X-API-KEY': APIKEY,
        'Content-Type': 'application/json'
    }
    payload = {
        'documents': [{
            'id': '1',
            'language': 'en',
            'text': text
        }]
    }
    url = "https://cent.ischool-iot.net/api/azure/text/sentiment"
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in Azure sentiment analysis: {e}")
        return {'error': str(e), 'status': 'REQUEST_FAILED'}

def get_azure_key_phrase_extraction(text: str) -> Dict[str, Any]:
    """
    Extract key phrases from text using Azure Text Analytics.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing key phrases
        Format: {'documents': [key_phrases], 'errors': []}
    """
    headers = {
        'X-API-KEY': APIKEY,
        'Content-Type': 'application/json'
    }
    payload = {
        'documents': [{
            'id': '1',
            'language': 'en',
            'text': text
        }]
    }
    url = "https://cent.ischool-iot.net/api/azure/text/keyphrases"
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in Azure key phrase extraction: {e}")
        return {'error': str(e), 'status': 'REQUEST_FAILED'}

def get_azure_named_entity_recognition(text: str) -> Dict[str, Any]:
    """
    Perform named entity recognition using Azure Text Analytics.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary containing recognized entities
        Format: {'documents': [entities], 'errors': []}
    """
    headers = {
        'X-API-KEY': APIKEY,
        'Content-Type': 'application/json'
    }
    payload = {
        'documents': [{
            'id': '1',
            'language': 'en',
            'text': text
        }]
    }
    url = "https://cent.ischool-iot.net/api/azure/text/entities"
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in Azure entity recognition: {e}")
        return {'error': str(e), 'status': 'REQUEST_FAILED'}

def geocode(place: str) -> Dict[str, Any]:
    '''
    Given a place name, return the latitude and longitude of the place.
    Written for example_etl.py
    
    Args:
        place: The location name to geocode
        
    Returns:
        Dictionary containing geocoding results
        Format: {'results': [geocoding_data], 'status': 'OK'}
    '''
    headers = {'X-API-KEY': APIKEY}
    params = {'location': place}
    url = "https://cent.ischool-iot.net/api/google/geocode"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in geocoding: {e}")
        return {'error': str(e), 'status': 'REQUEST_FAILED'}

def get_weather(lat: float, lon: float) -> Dict[str, Any]:
    '''
    Given a latitude and longitude, return the current weather at that location.
    written for example_etl.py
    
    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate
        
    Returns:
        Dictionary containing weather data
        Format: {'main': {weather_data}, 'coord': {lat, lon}}
    '''
    headers = {'X-API-KEY': APIKEY}
    params = {'lat': lat, 'lon': lon, 'units': 'imperial'}
    url = "https://cent.ischool-iot.net/api/weather/current"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return {'error': str(e), 'status': 'REQUEST_FAILED'}

# Test code (remove before submission)
if __name__ == "__main__":
    # Example test cases
    print("Testing Google Places API:")
    print(get_google_place_details("ChIJN1t_tDeuEmsRUsoyG83frY4"))
    
    print("\nTesting Azure Sentiment Analysis:")
    print(get_azure_sentiment("The food was excellent but the service was slow."))
    
    print("\nTesting Azure Key Phrase Extraction:")
    print(get_azure_key_phrase_extraction("The restaurant had great ambiance and delicious food."))
    
    print("\nTesting Azure Entity Recognition:")
    print(get_azure_named_entity_recognition("I visited Paris last summer and stayed at the Ritz Hotel."))
    
    print("\nTesting Geocoding:")
    print(geocode("Syracuse University"))
    
    print("\nTesting Weather API:")
    print(get_weather(43.0481, -76.1474))