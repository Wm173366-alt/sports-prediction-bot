from database.models import Match, Session
from datetime import datetime

session = Session()
matches = session.query(Match).filter(Match.date > datetime.utcnow()).all()

print(f"Total Upcoming Matches: {len(matches)}")
for m in matches:
    print(f"[{m.date}] {m.home_team.name} vs {m.away_team.name} (Sport: {m.sport})")
