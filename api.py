from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analysis.predictor import Predictor
from database.models import Match, Session, engine, Base
import uvicorn
import threading

# Initialize Database (ensure tables exist)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Google Antigravity Sports API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (App, Browser, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Welcome to Google Antigravity API"}

@app.get("/predictions")
def get_predictions():
    """
    Returns upcoming match predictions.
    """
    try:
        predictor = Predictor()
        results = predictor.predict_upcoming_matches()
        return {"count": len(results), "data": results}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Run on 0.0.0.0 to be accessible slightly easier if needed, though localhost is fine for emulator usually
    uvicorn.run(app, host="0.0.0.0", port=8000)
