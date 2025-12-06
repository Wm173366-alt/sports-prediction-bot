from database.models import init_db
from data_collection.football import FootballDataClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized.")

    logger.info("Fetching mock football data...")
    client = FootballDataClient()
    matches = client.fetch_upcoming_matches()
    
    logger.info(f"Saving {len(matches)} matches to DB...")
    count = client.save_matches(matches)
    logger.info(f"Saved {count} matches.")

if __name__ == "__main__":
    run()
