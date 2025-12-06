from database.models import Match, Session
from datetime import datetime

session = Session()
total_matches = session.query(Match).count()
upcoming_matches = session.query(Match).filter(Match.date > datetime.utcnow()).count()

print(f"Total Matches: {total_matches}")
print(f"Upcoming Matches (UTC > {datetime.utcnow()}): {upcoming_matches}")

if upcoming_matches > 0:
    first_match = session.query(Match).filter(Match.date > datetime.utcnow()).first()
    print(f"Sample Match: {first_match.sport} - {first_match.date}")
