from database.models import Match, Team, Session, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def view_data():
    teams = session.query(Team).all()
    print(f"--- TEAMS ({len(teams)}) ---")
    for t in teams:
        print(f"ID: {t.id} | {t.name} ({t.sport})")

    matches = session.query(Match).all()
    print(f"\n--- MATCHES ({len(matches)}) ---")
    for m in matches:
        home = session.query(Team).get(m.home_team_id).name
        away = session.query(Team).get(m.away_team_id).name
        print(f"[{m.date}] {home} vs {away} ({m.sport})")

if __name__ == "__main__":
    view_data()
