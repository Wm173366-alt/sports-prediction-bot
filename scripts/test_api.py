import os
import requests
from dotenv import load_dotenv

def test_key():
    load_dotenv()
    key = os.getenv("FOOTBALL_DATA_API_KEY")
    if not key:
        print("❌ No API Key found in .env")
        return

    print(f"🔑 Testing Key: {key[:4]}...{key[-4:]}")
    
    url = "https://api.football-data.org/v4/competitions"
    headers = {"X-Auth-Token": key}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ API Connection Successful!")
        print(f"   Available Competitions: {response.json()['count']}")
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"   Message: {response.json()}")

if __name__ == "__main__":
    test_key()
