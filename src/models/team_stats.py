from sqlalchemy import Column, Integer, String
from src.core.database import Base

class TeamStat(Base):
    __tablename__ = "team_stats"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, unique=True, index=True, nullable=False)
    group_letter = Column(String, nullable=False)
    total_points = Column(Integer, default=0)
    goals_scored = Column(Integer, default=0)
    goals_conceded = Column(Integer, default=0)