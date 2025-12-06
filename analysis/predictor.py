from data_collection.football import FootballDataClient
from database.models import Match, Session
from datetime import datetime
import random

class Predictor:
    def __init__(self):
        self.session = Session()
        # Fetch rankings once on init (in prod, should be refreshed)
        self.client = FootballDataClient()
        self.rankings = self.client.get_standings()

    def predict_upcoming_matches(self):
        matches = self.session.query(Match).filter(Match.date > datetime.utcnow()).order_by(Match.date).all()
        predictions = []
        
        for match in matches:
            home = match.home_team.name
            away = match.away_team.name

            if match.sport == 'basketball':
                # --- BASKETBALL LOGIC ---
                winner = random.choice([home, away])
                total_points = random.randint(200, 240)
                confidence = f"{random.randint(60, 90)}%"
                
                pred = {
                    "match": f"🏀 {home} vs {away}",
                    "date": match.date.strftime("%d/%m %H:%M"),
                    "sport": "basketball",
                    "prediction": f"{winner} (Vainqueur)",
                    "confidence": confidence,
                    "goals": f"Total Points: ~{total_points}",
                    "corners": "N/A",
                    "fouls": "N/A",
                    "yellow_cards": "N/A"
                }

            else:
                # --- FOOTBALL LOGIC ---
                # Default Stats if team not found in rankings
                home_stats = self.rankings.get(home, {"position": 10, "gf_avg": 1.5, "ga_avg": 1.2})
                away_stats = self.rankings.get(away, {"position": 10, "gf_avg": 1.5, "ga_avg": 1.2})
                
                # 1. Winner Logic (Based on Position difference)
                pos_diff = away_stats["position"] - home_stats["position"]
                
                if pos_diff > 5:
                    winner = home
                    conf_score = 0.75 + (pos_diff * 0.01)
                elif pos_diff < -5:
                    winner = away
                    conf_score = 0.75 + (abs(pos_diff) * 0.01)
                else:
                    winner = home 
                    conf_score = 0.55
                
                confidence = f"{min(int(conf_score * 100), 99)}%"

                # 2. Goals Logic
                avg_goals = (home_stats['gf_avg'] + away_stats['ga_avg'] + away_stats['gf_avg'] + home_stats['ga_avg']) / 2
                
                goals_pred = "Plus de 2.5" if avg_goals > 2.5 else "Moins de 2.5"
                total_goals_est = round(avg_goals)

                # 3. Stats Logic
                corners = int(9 + (home_stats['gf_avg'] + away_stats['gf_avg'])) 
                fouls = random.randint(20, 26) 
                yellow_cards = int(3 + (home_stats['ga_avg'] + away_stats['ga_avg']))

                pred = {
                    "match": f"⚽ {home} vs {away}",
                    "date": match.date.strftime("%d/%m %H:%M"),
                    "sport": "football",
                    "prediction": winner,
                    "confidence": confidence,
                    "goals": f"{goals_pred} (Est. {total_goals_est})",
                    "corners": corners,
                    "fouls": fouls,
                    "yellow_cards": yellow_cards
                }
            
            predictions.append(pred)
        
        # --- DAILY LIMITS ---
        MAX_FOOTBALL_PER_DAY = 15
        MAX_BASKETBALL_PER_DAY = 7
        
        football_preds = [p for p in predictions if p.get('sport') == 'football']
        basketball_preds = [p for p in predictions if p.get('sport') == 'basketball']
        
        # Take only the top N for each sport (already sorted by date)
        limited_football = football_preds[:MAX_FOOTBALL_PER_DAY]
        limited_basketball = basketball_preds[:MAX_BASKETBALL_PER_DAY]
        
        # Merge and re-sort by date
        final_predictions = limited_football + limited_basketball
        final_predictions.sort(key=lambda x: x['date'])
        
        return final_predictions

    def predict_football(self, match_data):
        # ... keep existing if needed or remove ...
        pass
