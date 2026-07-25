import sys
import os
import random
from sqlalchemy import text
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Ensure the root directory is on the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.database import SessionLocal
from src.models.team_stats import TeamStat
from src.models.news_documents import NewsDocument
from src.simulator import simulate_match


# =====================================================================
# Tool 1: Relational SQL Statistics Lookup
# =====================================================================
@tool
def get_team_stats_tool(team_name: str) -> str:
    """Useful for fetching official World Cup team statistics such as group letter, points, and goals scored/conceded."""
    db = SessionLocal()
    try:
        team = db.query(TeamStat).filter(TeamStat.team_name.ilike(team_name)).first()
        if not team:
            return f"No statistical record found for team: '{team_name}' in the 48-team database."
        return (
            f"Team: {team.team_name} | Group: {team.group_letter} | "
            f"Points: {team.total_points} | Goals Scored: {team.goals_scored} | "
            f"Goals Conceded: {team.goals_conceded}"
        )
    finally:
        db.close()


# =====================================================================
# Tool 2: Vector Similarity Search (RAG)
# =====================================================================
@tool
def search_tactical_news_tool(query: str) -> str:
    """Useful for searching tactical news, formation updates, and team strategies using vector search in pgvector."""
    db = SessionLocal()
    try:
        # Generate query vector (simulated 1536-dim embedding)
        mock_query_embedding = [random.uniform(-1, 1) for _ in range(1536)]
        embedding_str = f"[{','.join(map(str, mock_query_embedding))}]"
        
        # Execute L2 distance search (<->)
        sql_query = text(f"""
            SELECT title, content, embedding <-> '{embedding_str}' AS distance
            FROM news_documents
            ORDER BY distance ASC
            LIMIT 1;
        """)
        
        row = db.execute(sql_query).fetchone()
        if row:
            return f"Headline: {row.title}\nReport: {row.content} (Semantic Distance: {row.distance:.4f})"
        return "No relevant tactical reports found in the vector database."
    finally:
        db.close()


# =====================================================================
# Tool 3: Stage-Aware Monte Carlo Match Simulator
# =====================================================================
@tool
def simulate_match_tool(home_team: str, away_team: str, stage: str = "group") -> str:
    """Useful for running stage-aware Monte Carlo match simulations to predict win probabilities and goal expectations."""
    result = simulate_match(home_team, away_team, stage=stage, num_simulations=5000)
    probs = result["probabilities"]
    
    stage_formatted = stage.replace("_", " ").title()
    output = [
        f"--- Match Simulation: {home_team} vs {away_team} ({stage_formatted} Stage) ---",
        f"• {home_team} Win Probability: {probs.get(f'{home_team}_win', 'N/A')}",
        f"• Draw Probability: {probs.get('draw', 'N/A')}",
        f"• {away_team} Win Probability: {probs.get(f'{away_team}_win', 'N/A')}"
    ]
    return "\n".join(output)


# =====================================================================
# Tool 4: Open-World Live Web Search Fallback
# =====================================================================
@tool
def live_web_search_tool(query: str) -> str:
    """Useful for answering general questions, tournament rules, weather, or topics outside the local database."""
    try:
        search = DuckDuckGoSearchRun()
        result = search.invoke(query)
        return f"--- Live Web Search Result ---\n{result}"
    except Exception as e:
        return f"Live search unavailable for query: '{query}'. Error: {e}"


# =====================================================================
# Local Tool Suite Testing
# =====================================================================
def run_all_tools_test():
    print("=== Testing All Agent Tools ===")
    print("\n1. SQL Stat Tool:")
    print(get_team_stats_tool.invoke({"team_name": "Japan"}))
    
    print("\n2. Vector RAG Search Tool:")
    print(search_tactical_news_tool.invoke({"query": "high pressing counter"}))
    
    print("\n3. Match Simulator Tool (Knockout Stage):")
    print(simulate_match_tool.invoke({"home_team": "Argentina", "away_team": "Germany", "stage": "quarterfinal"}))
    
    print("\n4. Live Web Search Fallback Tool:")
    print(live_web_search_tool.invoke({"query": "FIFA World Cup 2026 substitution rules"}))


if __name__ == "__main__":
    run_all_tools_test()