import sys
import os

# Ensure the root directory is on the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import text
from src.core.database import engine, Base
from src.models.team_stats import TeamStat
from src.models.news_documents import NewsDocument

def init_db():
    print("Connecting to PostgreSQL container...")
    
    with engine.connect() as connection:
        # Enable the pgvector extension inside PostgreSQL
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        connection.commit()
        print("✓ pgvector extension enabled successfully.")

    # Create all tables defined in our SQLAlchemy models
    Base.metadata.create_all(bind=engine)
    print("✓ All tables ('team_stats', 'news_documents') created successfully!")

if __name__ == "__main__":
    init_db()