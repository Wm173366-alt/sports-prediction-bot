import os
import requests
from dotenv import load_dotenv

def test_standings():
    load_dotenv()
    key = os.getenv("FOOTBALL_DATA_API_KEY")
    headers = {"X-Auth-Token": key}
    
    # Premier League code is 'PL'
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Standings Access OK")
        table = data['standings'][0]['table']
        for team in table[:5]:
            print(f"{team['position']}. {team['team']['name']} (Points: {team['points']})")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_standings()
