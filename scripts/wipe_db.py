from database.models import Match, Team, Session, engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wipe_db():
    logger.info("⚠️ Wiping Database...")
    session = Session()
    try:
        session.query(Match).delete()
        session.query(Team).delete()
        session.commit()
        logger.info("✅ Database Cleaned (All matches and teams removed).")
    except Exception as e:
        logger.error(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    wipe_db()
