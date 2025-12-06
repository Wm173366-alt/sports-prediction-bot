print("Importing os...")
import os
print("Importing logging...")
import logging
logging.basicConfig(level=logging.INFO)

print("Importing database.models...")
try:
    from database.models import Match, Session
    print("Database models imported.")
except ImportError as e:
    print(f"Error importing database.models: {e}")

print("Importing data_collection.football...")
try:
    from data_collection.football import FootballDataClient
    print("FootballDataClient imported.")
except ImportError as e:
    print(f"Error importing data_collection.football: {e}")

print("Importing analysis.predictor...")
try:
    from analysis.predictor import Predictor
    print("Predictor imported.")
except ImportError as e:
    print(f"Error importing analysis.predictor: {e}")

print("Creating Predictor...")
try:
    p = Predictor()
    print("Predictor created.")
    results = p.predict_upcoming_matches()
    print(f"Predictions: {len(results)}")
except Exception as e:
    print(f"Crash during execution: {e}")
