from data_collection.football import FootballDataClient
from data_collection.basketball import BasketballDataClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_matches():
    logger.info("Starting daily match update...")
    
    # Football
    fb_client = FootballDataClient()
    fb_matches = fb_client.fetch_upcoming_matches()
    if fb_matches:
        count = fb_client.save_matches(fb_matches)
        logger.info(f"Successfully updated {count} football matches.")
    
    # Basketball
    bb_client = BasketballDataClient()
    bb_matches = bb_client.fetch_upcoming_matches()
    if bb_matches:
        count = bb_client.save_matches(bb_matches)
        logger.info(f"Successfully updated {count} basketball matches.")

if __name__ == "__main__":
    update_matches()
