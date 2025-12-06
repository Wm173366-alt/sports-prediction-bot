from analysis.predictor import Predictor
import logging

logging.basicConfig(level=logging.INFO)

try:
    print("Initializing Predictor...")
    p = Predictor()
    print("Running prediction...")
    results = p.predict_upcoming_matches()
    print(f"Predictions found: {len(results)}")
    if len(results) > 0:
        print(results[0])
except Exception as e:
    print(f"CRASH: {e}")
    import traceback
    traceback.print_exc()
