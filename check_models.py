import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: API Key not found.")
else:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("✅ AVAILABLE MODELS:")
        for model in response.json().get('models', []):
            if 'generateContent' in model['supportedGenerationMethods']:
                print(f"- {model['name']}") # This will print something like 'models/gemini-pro'
    else:
        print(f"❌ Error: {response.status_code} {response.text}")