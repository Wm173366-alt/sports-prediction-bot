from database.models import Team, Match, Session
from datetime import datetime, timedelta
import random

class BasketballDataClient:
    def __init__(self):
        self.session = Session()

    def fetch_upcoming_matches(self):
        """
        Generates mock upcoming basketball matches.
        """
        teams = ["Lakers", "Warriors", "Celtics", "Nets", "Bulls", "Heat", "Bucks", "Suns"]
        matches = []
        
        # Create 3 random matches for the next 2 days
        for i in range(3):
            home = random.choice(teams)
            away = random.choice([t for t in teams if t != home])
            
            # Random time between now and +2 days
            future_time = datetime.utcnow() + timedelta(days=random.randint(0, 1), hours=random.randint(1, 12))
            
            matches.append({
                "home": f"{home} (NBA)",
                "away": f"{away} (NBA)",
                "date": future_time,
                "sport": "basketball"
            })
            
        return matches

    def save_matches(self, matches_data):
        count = 0
        for m_data in matches_data:
            home_team = self._get_or_create_team(m_data["home"], m_data["sport"])
            away_team = self._get_or_create_team(m_data["away"], m_data["sport"])
            
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
