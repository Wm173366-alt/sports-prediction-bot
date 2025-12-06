from database.models import Team, Match, Session
from config.settings import FOOTBALL_DATA_API_KEY
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)

class FootballDataClient:
    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):
        self.session = Session()
        self.headers = {
            "X-Auth-Token": FOOTBALL_DATA_API_KEY
        }

    def fetch_upcoming_matches(self):
        """
        Fetches upcoming matches for major leagues (PL, PD, FL1, BL1, SA).
        """
        if not FOOTBALL_DATA_API_KEY:
            logger.warning("No API Key found for football-data.org. Using mock data.")
            return self._fetch_mock_matches()

        # Competitions: PL (Premier League), FL1 (Ligue 1), PD (Primera Division), BL1 (Bundesliga), SA (Serie A)
        competitions = ["PL", "FL1", "PD", "BL1", "SA"]
        all_matches = []

        for comp in competitions:
            try:
                url = f"{self.BASE_URL}/competitions/{comp}/matches"
                params = {
                    "status": "SCHEDULED",
                    "dateFrom": datetime.now().strftime("%Y-%m-%d"),
                    "dateTo": (datetime.now().date().replace(day=datetime.now().day + 3)).strftime("%Y-%m-%d") # Next 3 days
                }
                response = requests.get(url, headers=self.headers, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    for match in data.get("matches", []):
                        all_matches.append({
                            "home": match["homeTeam"]["name"],
                            "away": match["awayTeam"]["name"],
                            "date": datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ"),
                            "sport": "football"
                        })
                else:
                    logger.error(f"Failed to fetch {comp}: {response.status_code} {response.text}")
            except Exception as e:
                logger.error(f"Error fetching {comp}: {e}")

        return all_matches

    def get_standings(self):
        """
        Fetches standings for major leagues to empower the predictor.
        Returns a dict: {'Team Name': {'position': 1, 'points': 80, 'goals_per_match': 2.1}}
        """
        if not FOOTBALL_DATA_API_KEY:
            return {}

        competitions = ["PL", "FL1", "PD", "BL1", "SA"]
        rankings = {}

        for comp in competitions:
            try:
                url = f"{self.BASE_URL}/competitions/{comp}/standings"
                response = requests.get(url, headers=self.headers, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    for standing in data['standings']:
                        if standing['type'] == 'TOTAL':
                            for entry in standing['table']:
                                team_name = entry['team']['name']
                                played = entry['playedGames']
                                goals_for = entry['goalsFor']
                                goals_against = entry['goalsAgainst']
                                
                                rankings[team_name] = {
                                    "position": entry['position'],
                                    "points": entry['points'],
                                    "gf_avg": round(goals_for / played, 2) if played > 0 else 0,
                                    "ga_avg": round(goals_against / played, 2) if played > 0 else 0
                                }
            except Exception:
                continue
        
        return rankings

    def _fetch_mock_matches(self):
        from datetime import timedelta
        return [
            {"home": "PSG (Mock)", "away": "Marseille (Mock)", "date": datetime.utcnow() + timedelta(days=1), "sport": "football"},
            {"home": "Real Madrid (Mock)", "away": "Barcelona (Mock)", "date": datetime.utcnow() + timedelta(days=2), "sport": "football"},
        ]

    def save_matches(self, matches_data):
        """
        Saves matches to the database, creating Teams if they don't exist.
        """
        count = 0
        for m_data in matches_data:
            # 1. Get or Create Teams
            home_team = self._get_or_create_team(m_data["home"], m_data["sport"])
            away_team = self._get_or_create_team(m_data["away"], m_data["sport"])
            
            # Check if match already exists
            existing = self.session.query(Match).filter_by(
                home_team_id=home_team.id, 
                away_team_id=away_team.id,
                date=m_data["date"]
            ).first()

            if not existing:
                match = Match(
                    sport=m_data["sport"],
                    date=m_data["date"],
                    home_team_id=home_team.id,
                    away_team_id=away_team.id
                )
                self.session.add(match)
                count += 1
        
        self.session.commit()
        return count

    def _get_or_create_team(self, name, sport):
        team = self.session.query(Team).filter_by(name=name, sport=sport).first()
        if not team:
            team = Team(name=name, sport=sport)
            self.session.add(team)
            self.session.commit()
        return team
