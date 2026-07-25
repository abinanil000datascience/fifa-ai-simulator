import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.core.database import SessionLocal
from src.models.team_stats import TeamStat
from src.models.news_documents import NewsDocument
from src.simulator import simulate_match
from src.brain import process_user_query
from dotenv import load_dotenv

load_dotenv()  # Reads the .env file automatically

app = FastAPI(
    title="FIFA 2026 Autonomous Simulator API",
    description="Enterprise API powering team stats, predictive analytics, vector search, and AI Agents.",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "online", "system": "FIFA 2026 AI Engine"}

@app.get("/teams")
def get_all_teams(db: Session = Depends(get_db)):
    """Fetch all registered 48 FIFA World Cup teams and their current standings."""
    return db.query(TeamStat).all()

@app.get("/news")
def get_all_news(db: Session = Depends(get_db)):
    """Fetch all stored tactical news and reports."""
    news = db.query(NewsDocument.id, NewsDocument.title, NewsDocument.content, NewsDocument.created_at).all()
    return [{"id": n.id, "title": n.title, "content": n.content, "created_at": n.created_at} for n in news]

@app.get("/search/news")
def search_news_vector(limit: int = Query(2, ge=1, le=10), db: Session = Depends(get_db)):
    """Performs vector similarity search using pgvector's L2 distance operator (<->)."""
    import random
    sample_query_embedding = [random.uniform(-1, 1) for _ in range(1536)]
    embedding_str = f"[{','.join(map(str, sample_query_embedding))}]"
    
    sql_query = text(f"""
        SELECT id, title, content, embedding <-> '{embedding_str}' AS distance
        FROM news_documents
        ORDER BY distance ASC
        LIMIT :limit;
    """)
    
    result = db.execute(sql_query, {"limit": limit}).fetchall()
    return [{"id": row.id, "title": row.title, "content": row.content, "distance": float(row.distance)} for row in result]

@app.get("/simulate")
def run_match_simulation(
    home_team: str = Query("Portugal", description="Home team name"),
    away_team: str = Query("Spain", description="Away team name"),
    simulations: int = Query(5000, ge=100, le=50000, description="Number of Monte Carlo runs"),
    stage: str = Query("group", description="Stage of the tournament")
):
    """Executes a Monte Carlo simulation between two teams based on Poisson probability distributions."""
    return simulate_match(home_team, away_team, stage=stage, num_simulations=simulations)

@app.post("/agent/chat")
def agent_chat_endpoint(payload: ChatRequest):
    """
    Accepts natural language prompts and delegates execution to the autonomous AI Agent pipeline.
    """
    return process_user_query(payload.prompt)