from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config.settings import DB_PATH

Base = declarative_base()
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
Session = sessionmaker(bind=engine)

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    sport = Column(String, nullable=False) # 'football' or 'basketball'
    
class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    sport = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    home_team_id = Column(Integer, ForeignKey('teams.id'))
    away_team_id = Column(Integer, ForeignKey('teams.id'))
    
    # Scores (nullable if match hasn't happened)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    prediction_type = Column(String) # 'winner', 'goals_over_2.5', 'total_points'
    prediction_value = Column(String) # 'Home', 'Over', '210'
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    match = relationship("Match")

def init_db():
    Base.metadata.create_all(engine)
