"""List available Google AI models using REST API."""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file")
    exit(1)

print("Available Google AI Models:")
print("=" * 80)

# Use the Generative Language API to list models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if "models" in data:
        for model in data["models"]:
            name = model.get("name", "").replace("models/", "")
            display_name = model.get("displayName", "N/A")
            description = model.get("description", "N/A")
            
            # Check if it supports generateContent
            methods = model.get("supportedGenerationMethods", [])
            if "generateContent" in methods:
                print(f"\n✓ {name}")
                print(f"  Display Name: {display_name}")
                print(f"  Description: {description[:100]}...")
                
                # Show token limits if available
                if "inputTokenLimit" in model:
                    print(f"  Input Token Limit: {model['inputTokenLimit']:,}")
                if "outputTokenLimit" in model:
                    print(f"  Output Token Limit: {model['outputTokenLimit']:,}")
    else:
        print("No models found in response")
        print(f"Response: {data}")
        
except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response body: {e.response.text}")
except Exception as e:
    print(f"Unexpected error: {e}")

print("\n" + "=" * 80)
print("\nCommon models you can use:")
print("  - gemini-2.0-flash-exp (experimental, latest)")
print("  - gemini-1.5-pro")
print("  - gemini-1.5-flash")
print("  - gemini-1.0-pro")
